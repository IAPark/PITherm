import os
import sys
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))

from ForcedAir import app as application
import ForcedAir
ForcedAir.AC_pin_number = 17
ForcedAir.heater_pin_number = 18
ForcedAir.fan_pin_number = 4
