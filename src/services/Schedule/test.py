import subprocess
import unittest
from datetime import datetime

import requests
import time
from pymongo import MongoClient


class TestSchedule(unittest.TestCase):
    url = "http://localhost:5003"
    schedule = subprocess.Popen(["python", ["Schedule.py"]])

    def test_add_to_schedule(self):
        requests.post(self.url + "/schedule/", json={
                                                        "start": 10,
                                                        "end": 10,
                                                        "state": {
                                                            "AC_target": 100,
                                                            "heater_target": 0,
                                                            "fan": False
                                                        }
                                                    })
        r = requests.get(self.url + "/schedule/")
        self.assertEquals(r.json()["data"][0]["start"], 10)
        self.assertEquals(r.json()["data"][0]["end"], 10)
        self.assertEquals(r.json()["data"][0]["state"],
                          {
                              "AC_target": 100,
                              "heater_target": 0,
                              "fan": False
                          })
        self.assertEquals(len(r.json()["data"]), 1)

    def test_add_to_schedule_weekly(self):
        requests.post(self.url + "/schedule/weekly/", json={
                                                        "week_time": 10,
                                                        "state": {
                                                            "AC_target": 100,
                                                            "heater_target": 0,
                                                            "fan": False
                                                        }
                                                    })
        r = requests.get(self.url + "/schedule/weekly/")
        self.assertEquals(r.json()["data"][0]["week_time"], 10)
        self.assertEquals(r.json()["data"][0]["state"],
                          {
                              "AC_target": 100,
                              "heater_target": 0,
                              "fan": False
                          })
        self.assertEquals(len(r.json()["data"]), 1)

    def test_current(self):
        now = int(time.time())

        requests.post(self.url + "/schedule/", json={
            "start": now,
            "end": now + 10,
            "state": {
                "AC_target": 100,
                "heater_target": 0,
                "fan": False
            }
        })

        requests.post(self.url + "/schedule/", json={
            "start": now - 10,
            "end": now,
            "state": {
                "AC_target": 100,
                "heater_target": 0,
                "fan": True
            }
        })

        requests.post(self.url + "/schedule/", json={
            "start": now + 3,
            "end": now + 100,
            "state": {
                "AC_target": 100,
                "heater_target": 0,
                "fan": True
            }
        })

        r = requests.get(self.url + "/schedule/current")
        self.assertEquals(r.json()["data"]["start"], now)
        self.assertEquals(r.json()["data"]["end"], now + 10)
        self.assertEquals(r.json()["data"]["state"],
                          {
                              "AC_target": 100,
                              "heater_target": 0,
                              "fan": False
                          })

    def test_current_weekly(self):
        now = datetime.utcnow().weekday() * 24 * 60 ** 2 + (datetime.utcnow().hour * 60 + datetime.utcnow().minute) * 60

        requests.post(self.url + "/schedule/weekly/", json={
            "week_time": now + 10,
            "state": {
                "AC_target": 0,
                "heater_target": 0,
                "fan": True
            }
        })

        requests.post(self.url + "/schedule/weekly/", json={
            "week_time": now - 10,
            "state": {
                "AC_target": 100,
                "heater_target": 0,
                "fan": False
            }
        })

        requests.post(self.url + "/schedule/weekly/", json={
            "week_time": now - 11,
            "state": {
                "AC_target": 120,
                "heater_target": 0,
                "fan": True
            }
        })
        time.sleep(1)
        r = requests.get(self.url + "/schedule/weekly/current")
        self.assertEquals(r.json()["data"]["week_time"], now - 10)
        self.assertEquals(r.json()["data"]["state"],
                          {
                              "AC_target": 100,
                              "heater_target": 0,
                              "fan": False
                          })

    def test_get_state_defaults_to_non_weekly(self):
        unix_time = int(time.time())
        requests.post(self.url + "/schedule/", json={
            "start": unix_time,
            "end": unix_time + 10,
            "state": {
                "AC_target": 160,
                "heater_target": 0,
                "fan": False
            }
        })

        now = datetime.utcnow().weekday() * 24 * 60 ** 2 + (datetime.utcnow().hour * 60 + datetime.utcnow().minute) * 60
        requests.post(self.url + "/schedule/weekly/", json={
            "week_time": now - 10,
            "state": {
                "AC_target": 100,
                "heater_target": 0,
                "fan": True
            }
        })

        r = requests.get(self.url + "/state/" + str(unix_time + 3))

        self.assertEquals(r.json()["data"],
                          {
                              "AC_target": 160,
                              "heater_target": 0,
                              "fan": False
                          })

    def test_get_state_use_weekly(self):
        unix_time = int(time.time())
        now = datetime.utcnow().weekday() * 24 * 60 ** 2 + (datetime.utcnow().hour * 60 + datetime.utcnow().minute) * 60
        requests.post(self.url + "/schedule/weekly/", json={
            "week_time": now - 10,
            "state": {
                "AC_target": 100,
                "heater_target": 0,
                "fan": True
            }
        })

        r = requests.get(self.url + "/state/" + str(unix_time + 3))

        self.assertEquals(r.json()["data"],
                          {
                              "AC_target": 100,
                              "heater_target": 0,
                              "fan": True
                          })


    @classmethod
    def tearDownClass(cls):
        cls.schedule.kill()
        cls.schedule.terminate()

    def setUp(self):
        client = MongoClient()
        client.PITherm.state_changes_weekly.remove()
        client.PITherm.state_changes.remove()

    def tearDown(self):
        self.schedule.kill()
        self.schedule.terminate()
