import os
import sys
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))

from run import app as application
from run import AC_pin
from run import heater_pin
from run import fan_pin
import run
run.AC_pin = 17
run.heater_pin = 18
run.fan_pin = 4
