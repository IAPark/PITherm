from time import sleep

from backend.router import Router
from ticker import default_ticker
import services
from services.temp_monitor import TempMonitor
from hardware_abstraction import TemperatureSensor, Pin

services.TempMonitor = TempMonitor(TemperatureSensor(0x48))
from services.database import DB
services.DB = DB()
from services.air_handler import AirHandler
from debugging import FakePin
services.AirHandler = AirHandler(AC_pin=Pin(4), fan_pin=FakePin("fan"), heater_pin=FakePin("heater"), db=services.DB)

router = Router()
import debugging
from API_backend import general


def start(command_queue, response_queue):
    router.command_queue = command_queue
    router.response_queue = response_queue
    while True:
        default_ticker.tick_all()
        router.handle()
        sleep(1)
