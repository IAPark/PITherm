import sys

from src.TemperatureMonitor import TemperatureMonitor
from src.temperature import TemperatureSensor

import argparse

parser = argparse.ArgumentParser(description='Broadcast temperatures to URLs')
parser.add_argument('observers', metavar='N', type=str, nargs='+',
                   help='the observers', default=())
parser.add_argument("-i", "--interval", type=int, help="the period between testing the temperature", default=60)
parser.add_argument("-s", "--smoothing", type=int, help="the number of samples to average when broadcasting a result", default=60)

args = parser.parse_args()

SENSOR_ADDRESS = 0x48

tempMonitor = TemperatureMonitor(TemperatureSensor(SENSOR_ADDRESS),
                                 interval=args.interval,
                                 smoothing=args.smoothing,
                                 observers=args.observers)
tempMonitor.run()
