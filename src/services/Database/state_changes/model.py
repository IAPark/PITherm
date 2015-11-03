from datetime import datetime
from bson import ObjectId
from pymongo import MongoClient

client = MongoClient()
db = client.PITherm


class StateChange:
    collection = db.state_changes

    def __init__(self, start, end, AC_target, heater_target, fan, id=None):
        self.id = id
        self.start = start
        self.end = end
        self.AC_target = AC_target
        self.heater_target = heater_target
        self.fan = fan

        assert type(start) is datetime
        assert type(end) is datetime
        assert type(AC_target) is int or float
        assert type(heater_target) is int or float
        assert type(fan) is int or float

    @classmethod
    def remove(cls, to_remove):
        return cls.collection.remove({"_id": ObjectId(to_remove)})

    @classmethod
    def from_dictionary(cls, json):
        start = json["start"]
        if type(start) is not datetime:
            start = datetime.utcfromtimestamp(json["start"])
        end = json["end"]
        if type(end) is not datetime:
            end = datetime.utcfromtimestamp(json["end"])
        AC_target = json["state"]["AC_target"]
        heater_target = json["state"]["heater_target"]
        fan = json["state"]["fan"]

        try:
            id = json["_id"]["$oid"]
        except KeyError:
            id = None
        except TypeError:
            try:
                id = ObjectId(json["_id"])
            except:
                id = None

        return cls(start, end, AC_target, heater_target, fan, id=id)


    @classmethod
    def get_current(cls, now):
        result = cls.collection.find_one({"start": {"$lte": now}, "end": {"$gte": now}})
        if result is None:
            return None
        return cls.from_dictionary(result)

    @classmethod
    def get_next(cls, now):
        print("get_next")
        result = cls.collection.find_one({"$query": {"start": {"$gte": now}}, "$orderby": {"now": 1}})
        if result is None:
            return None

        return cls.from_dictionary(result)

    @classmethod
    def get_all(cls):
        results = cls.collection.find()
        state_changes = []
        for result in results:
            state_changes.append(cls.from_dictionary(result))

        return state_changes

    def save(self):
        delayed_state_change = {
            "start": self.start,
            "end": self.end,
            "state": {"AC_target": self.AC_target, "heater_target": self.heater_target, "fan": self.fan}
        }
        if self.id is not None:
            delayed_state_change["_id"] = self.id

        return self.collection.save(delayed_state_change)

    def to_dictionary(self):
        return {"start": int((self.start-datetime(1970,1,1)).total_seconds()),
                "end": int((self.end-datetime(1970,1,1)).total_seconds()),
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