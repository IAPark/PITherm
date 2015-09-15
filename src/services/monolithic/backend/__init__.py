from src.services.backend import Router
from src.services.monolithic.services import default_ticker
from src.services import services
from src.services.services.temp_monitor import TempMonitor
from src.services.hardware_abstraction import TemperatureSensor, Pin

services.TempMonitor = TempMonitor(TemperatureSensor(0x48))
from src.services.database import temp_log

reload(temp_log)
from src.services.services.air_handler import AirHandler
from debugging import FakePin
services.AirHandler = AirHandler(AC_pin=Pin(4), fan_pin=FakePin("fan"), heater_pin=FakePin("heater"))

router = Router()
import debugging
from API_backend import general


def start(command_queue, response_queue):
    print("started backend")
    router.command_queue = command_queue
    router.response_queue = response_queue
    while True:
        default_ticker.tick_all()
        router.handle()
