import time

import requests


class TemperatureMonitor:
    def __init__(self, temperature_sensor, interval = 60, smoothing: int=5, observers=()):
        self.temperature_sensor = temperature_sensor
        self.interval = interval
        self.smoothing = smoothing
        self.observers = observers
        self.history = []

    def run(self):
        while True:
            self.check_temp()
            time.sleep(self.interval)

    def check_temp(self):
        self.history = self.history[:self.smoothing-1]
        self.history.append(self.temperature_sensor.get_temp())

        sum = 0.0
        for temp in self.history:
            sum += temp

        average = sum / len(self.history)

        self.report(average)

    def report(self, temp: float):
        for observer in self.observers:
            requests.post(observer, json={"temp": temp})
