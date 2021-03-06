from datetime import datetime

from bson import ObjectId

from . import temps


class TempLog:
    def __init__(self, date, temp, id=None):
        self.id = id
        self.date = date
        self.temp = temp

        assert type(date) is datetime
        assert type(temp) is float or int

    def save(self):
        to_save = {
            "temp": self.temp,
            "date": self.date
        }

        if self.id is not None:
            to_save["_id"] = self.id

        return temps.save(to_save)

    @classmethod
    def from_dictionary(cls, json):
        date = json["date"]
        if type(date) is not datetime:
            date = datetime.utcfromtimestamp(json["date"])

        temp = json["temp"]

        try:
            id = json["_id"]["$oid"]
        except KeyError:
            id = None
        except TypeError:
            try:
                id = ObjectId(json["_id"])
            except:
                id = None

        return cls(date, temp, id=id)

    def to_dictionary(self):
        return {"date": int(self.date.strftime("%s")),
                "_id": str(self.id),
                "temp": self.temp}

    @classmethod
    def get_all(cls):
        results = temps.find({}, {"date": -1, "temp": 1})
        temp_changes = []
        for result in results:
            temp_changes.append(cls.from_dictionary(result))

        return temp_changes

    @classmethod
    def get_all_dic(cls):
        all_items = cls.get_all()
        result = []
        for item in all_items:
            result.append(item.to_dictionary())
        return result