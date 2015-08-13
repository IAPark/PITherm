__author__ = 'Isaac'
from router import Router
from services import Services
from services.temp_monitor import TempMonitor
from services.air_handler import AirHandler
from hardware_abstraction import Pin, TemperatureSensor
from multiprocessing import Queue

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
router = Router()

def centigrade_to_fahrenheit(c):
    return c * 1.8000 + 32

def main_loop(command_queue, return_queue):
    """
    @type return_queue: Queue
    @type command_queue: Queue
    """

    try:
        command = command_queue.get(blocking=False)
        if command is not None:
            url = None
            try:
                url = command["url"]
                return_queue.put({"url": url, "body": router[url](command["body"])})
            except KeyError:
                print("could not handle " + str(url))
    except Queue.Empty:
        pass
    Services.TempMonitor.check_temp()
    print("temp: " + str(centigrade_to_fahrenheit(Services.TempMonitor.last_temp)) + "(F), " + str(Services.TempMonitor.last_temp))
    time.sleep(1)


@router.route("/temp")
def get_temp(body):
    return Services.TempMonitor.last_temp


def start(command_queue, return_queue):
    while True:
        main_loop(command_queue, return_queue)