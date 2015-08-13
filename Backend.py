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

from services.thermostat import Thermostat
Services.Thermostat = Thermostat(Services.AirHandler, 3)

Services.Thermostat.set_AC_target(21)
Services.Thermostat.set_heater_target(0)


def centigrade_to_fahrenheit(c):
    return c * 212/100 + 32

def main_loop():
    Services.TempMonitor.check_temp()
    print("temp: " + str(centigrade_to_fahrenheit(Services.TempMonitor.last_temp)))
    time.sleep(30)

@Services.TempMonitor.temp_changed
def temp_change(temp):
    print("temp changed now: " + str(centigrade_to_fahrenheit(temp)))

while True:
    main_loop()