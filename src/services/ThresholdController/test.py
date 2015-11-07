import subprocess
import unittest
import requests
from multiprocessing import Process, Queue
from multiprocessing.queues import Empty
import time

from TestingServices import FakeForcedAirController
from TestingServices import FakeSchedule


class SetTemp(unittest.TestCase):
    url = "http://localhost:5000/temp"

    def setUp(self):
        self.FAC_queue = Queue()
        self.schedule_queue = Queue()

        self.FAC = Process(target=FakeForcedAirController.run, args=(self.FAC_queue,))
        self.schedule = Process(target=FakeSchedule.run, args=(self.schedule_queue,))
        self.FAC.start()
        self.schedule.start()

        self.tc = subprocess.Popen(["python", "ThresholdController.py",
                                    "http://localhost:" + str(FakeForcedAirController.port),
                                    "http://localhost:" + str(FakeSchedule.port), "3"])
        time.sleep(0.1)
        self.assertEquals(self.tc.poll(), None, "can't run ThresholdController")

    def test_temp_above_temp(self):
        self.schedule_queue.put({"AC_target": 12, "heat_target": 0, "fan": False})
        requests.post(self.url, json={"temp": 16})
        time.sleep(0.1)
        try:
            self.assertEquals(self.FAC_queue.get(block=False), {"ac": True})
        except Empty:
            self.fail("Nothing was sent to Forced Air Controller")

    def test_temp_within_upper_threshold(self):
        self.schedule_queue.put({"AC_target": 12,"heat_target": 0, "fan": False})
        requests.post(self.url, json={"temp": 13})
        time.sleep(0.1)
        with self.assertRaises(Empty):
            self.FAC_queue.get(block=False)

    def test_temp_within_bounds(self):
        self.schedule_queue.put({"AC_target": 12,"heat_target": 0, "fan": False})
        requests.post(self.url, json={"temp": 10})
        time.sleep(0.1)
        self.assertEquals(list(self.FAC_queue.get(block=False).values())[0], False)
        self.assertEquals(list(self.FAC_queue.get(block=False).values())[0], False)
        with self.assertRaises(Empty):
            self.FAC_queue.get(block=False)

    def test_temp_below_temp(self):
        self.schedule_queue.put({"AC_target": 12, "heat_target": 0, "fan": False})
        requests.post(self.url, json={"temp": -5})
        time.sleep(0.1)
        try:
            self.assertEquals(self.FAC_queue.get(block=False), {"heater": True})
        except Empty:
            self.fail("Nothing was sent to Forced Air Controller")

    def test_temp_within_lower_threshold(self):
        self.schedule_queue.put({"AC_target": 12,"heat_target": 0, "fan": False})
        requests.post(self.url, json={"temp": -1})
        time.sleep(0.1)
        with self.assertRaises(Empty):
            print(self.FAC_queue.get(block=False))

    def tearDown(self):
        self.tc.kill()
        self.FAC.terminate()
        self.schedule.terminate()
        self.assertEquals(self.tc.poll(), None, "TC exited early")
        self.tc.terminate()


if __name__ == '__main__':
    unittest.main()
