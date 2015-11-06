from bson import ObjectId
from pymongo import MongoClient

from .. import state_changes

client = MongoClient()
db = client.PITherm


class StateChangeWeekly(state_changes.StateChange):
    collection = db.state_changes_weekly

    def __init__(self, seconds_into_week, AC_target, heater_target, fan, id=None):
        self.id = id
        self.seconds_into_week = seconds_into_week
        self.AC_target = AC_target
        self.heater_target = heater_target
        self.fan = fan

        assert type(seconds_into_week) is int
        assert type(AC_target) is int or float
        assert type(heater_target) is int or float
        assert type(fan) is int or float

    @classmethod
    def from_dictionary(cls, json):
        seconds_into_week = json["week_time"]

        AC_target = json["state"]["AC_target"]
        heater_target = json["state"]["heater_target"]
        fan = json["state"]["fan"]

        try:
            id = ObjectId(json["_id"]["$oid"])
        except KeyError:
            id = None
        except TypeError:
            try:
                id = ObjectId(json["_id"])
            except:
                id = None

        return cls(seconds_into_week, AC_target, heater_target, fan, id=id)


    @classmethod
    def get_current(cls, now):
        week_time = now.weekday() * 24 * 60 ** 2 + (now.hour * 60 + now.minute) * 60
        result = cls.collection.aggregate(
            [
                {"$project": {
                    "time_delta": {"$mod": [{"$add": [{"$subtract": [week_time, "$week_time"]}, 24 * 7 * 60 ** 2]},
                                            24 * 7 * 60 ** 2]},
                    "state": 1,
                    "week_time": 1}
                },
                {"$sort": {"time_delta": 1}}
            ]).next()
        return cls.from_dictionary(result)

    @classmethod
    def get_next(cls, now):
        week_time = now.weekday() * 24 * 60 ** 2 + (now.hour * 60 + now.minute) * 60
        result = cls.collection.aggregate(
            [
                {"$project": {
                    "time_delta": {"$mod": [{"$add": [{"$subtract": [week_time, "$week_time"]}, 24 * 7 * 60 ** 2]},
                                            24 * 7 * 60 ** 2]},
                    "state": 1,
                    "week_time": 1}
                },
                {"$sort": {"time_delta": -1}}
            ]).next()
        return cls.from_dictionary(result)

    def save(self):
        delayed_state_change = {
            "week_time": self.seconds_into_week,
            "state": {"AC_target": self.AC_target, "heater_target": self.heater_target, "fan": self.fan}
        }
        if self.id is not None:
            delayed_state_change["_id"] = self.id

        return self.collection.save(delayed_state_change)

    def to_dictionary(self):
        return {"week_time": self.seconds_into_week,
                "_id": str(self.id),
                "state": {"AC_target": self.AC_target,
                          "heater_target": self.heater_target,
                          "fan": self.fan}}

    @classmethod
    def get_all_dic(cls):
        all_items = cls.get_all()
        result = []
        for item in all_items:
            result.append(item.to_dictionary())
        return result

