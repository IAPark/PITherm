__author__ = 'Isaac'
from services import Services
from services.temp_monitor import TempMonitor
from services.air_handler import AirHandler
from hardware_abstraction import Pin, TemperatureSensor

class FakePin:

    def __init__(self, name):
        self.name = name
        self.state = False

    def sense(self):
        return False

    def set(self, state):
        self.state = state


    def get(self):
        return self.state

Services.TempMonitor = TempMonitor(TemperatureSensor(0x48))
from services.database import DB
Services.DB = DB()
Services.AirHandler = AirHandler(AC_pin=Pin(4), fan_pin=FakePin("fan"), heater_pin=FakePin("heater"), db=Services.DB)
import time

from Services.thermostat import Thermostat
Services.Thermostat = Thermostat(Services.AirHandler, 3)


def main_loop():
    Services.TempMonitor.check_temp()
    time.sleep(30)

@Services.TempMonitor.temp_changed
def temp_change(temp):
    print("temp now: " + str(temp))

while True:
    main_loop()