from datetime import datetime
from database import states


class StateLog:
    collection = states

    def __init__(self, date, AC, heater, fan, id=None):
        self.id = id
        self.date = date
        self.AC = AC
        self.heater = heater
        self.fan = fan

        assert type(date) is datetime
        assert type(AC) is bool
        assert type(heater) is bool
        assert type(fan) is bool

    def save(self):
        to_save = {
            "date": self.date,
            "state": {"AC": self.AC, "heater": self.heater, "fan": self.fan}
        }

        if self.id is not None:
            to_save["_id"] = self.id

        return self.collection.save(to_save)

    @classmethod
    def from_dictionary(cls, json):
        date = json["date"]
        if type(date) is not datetime:
            date = datetime.utcfromtimestamp(json["date"])

        AC = json["state"]["AC"]
        heater = json["state"]["heater"]
        fan = json["state"]["fan"]

        try:
            id = json["_id"]["$oid"]
        except TypeError:
            try:
                id = json["_id"]
            except KeyError:
                id = None

        return cls(date, AC, heater, fan, id=id)

    def to_dictionary(self):
        return {"date": int(self.date.strftime("%s")),
                "_id": self.id,
                "state": {"AC": self.AC, "heater": self.heater, "fan": self.fan}}

    @classmethod
    def get_all(cls):
        results = cls.collection.find()
        state_changes = []
        for result in results:
            state_changes.append(cls.from_dictionary(result))

        return state_changes


    @classmethod
    def get_all_dic(cls):
        all_items = cls.get_all()
        result = []
        for item in all_items:
            result.append(item.to_dictionary())
        return result
