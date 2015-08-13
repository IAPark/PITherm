__author__ = 'Isaac'
from pymongo import MongoClient
from datetime import datetime
from services import Services

temp_monitor = Services.TempMonitor

class DB:
    self = None
    def __init__(self):
        DB.self = self
        self.client = MongoClient()
        self.db = self.client.PITherm
        self.temps = self.db.temps
        self.states = self.db.states
        self.repeating_schedule = self.db.repeating_schedule
        self.schedule = self.db.schedule

    def log_temp_change(self, temp: int):
        """Method to be called every time the temperature changes.

        Shouldn't need to be changed by the user, but can be
         """
        temp_change = {
            "temp": temp,
            "date": datetime.utcnow()
        }
        self.temps.insert_one(temp_change)


    def log_air_handler_state(self, AC, heater, fan):
        state_change = {
            "state": {"AC": AC, "heater": heater, "fan": fan},
            "date": datetime.utcnow()
            }
        self.states.insert_one(state_change)

    def set_delayed_state_change(self, start: datetime, end: datetime, AC_target: int, heater_target: int, fan: bool):
        delayed_state_change = {
            "start": start,
            "end": end,
            "state": {"AC_target": AC_target, "heater_target": heater_target, "fan": fan}

        }
        self.schedule.insert_one(delayed_state_change)

    def set_repeating_state_change(self, seconds_into_week: int, AC_target: int, heater_target: int, fan: bool):
        repeating_state_change = {
            "week_time": seconds_into_week,
            "state": {"AC_target": AC_target, "heater_target": heater_target, "fan": fan}
        }
        self.repeating_schedule.insert_one(repeating_state_change)

    def get_scheduled_state(self, now: datetime):
        now = now.utcnow()
        return self.schedule.find_one({"start": {"$lt": now}, "end": {"$gt": now}})

    def get_repeating_change(self, now: datetime):
        week_time = now.weekday() * 24 * 60**2 + (now.hour*60 + now.minute)*60

        return self.repeating_schedule.aggregate(
            [
                {"$project": {
                    "time_delta": {"$mod": [{"$add": [{"$subtract": [week_time, "$week_time"]}, 24*7*60**2]}, 24*7*60**2]},
                    "state": 1,
                    "week_time": 1}
                 },
                {"$sort": {"time_delta": 1}}
            ]).next()

    @staticmethod
    @temp_monitor.temp_changed
    def temp_changed(temp: int):
        DB.self.log_temp_change(temp)