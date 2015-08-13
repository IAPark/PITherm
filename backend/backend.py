__author__ = 'Isaac'
from router import Router
from services import Services
from services.temp_monitor import TempMonitor
from services.air_handler import AirHandler
from hardware_abstraction import Pin, TemperatureSensor
from multiprocessing.queues import Queue

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
router = Router(None, None)

def centigrade_to_fahrenheit(c):
    return c * 1.8000 + 32

def main_loop():
    global router

    router.handle()
    Services.TempMonitor.check_temp()
    print("temp: " + str(centigrade_to_fahrenheit(Services.TempMonitor.last_temp)) + "(F), " + str(Services.TempMonitor.last_temp))

    time.sleep(1)


@router.route("/temp")
def get_temp():
    return Services.TempMonitor.last_temp

@router.route("/temps")
def get_temps():
    return list(Services.DB.temps.find().sort({"date": 1}))


def start(command_queue, response_queue):
    global router
    router.command_queue = command_queue
    router.response_queue = response_queue
    while True:
        main_loop()