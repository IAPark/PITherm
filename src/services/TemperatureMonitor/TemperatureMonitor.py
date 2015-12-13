import sys

from src.TemperatureMonitor import TemperatureMonitor
from src.temperature import TemperatureSensor

SENSOR_ADDRESS = 0x48

tempMonitor = TemperatureMonitor(TemperatureSensor(SENSOR_ADDRESS), observers=sys.argv[1:])
tempMonitor.run()
