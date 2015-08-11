# Thermostat controls the AC, Heater, and Fan

from air_handler import AirHandler
from temp_monitor import TempMonitor
from constants import *

temp_monitor = TempMonitor(Te)


class Thermostat:
    thermostats = []
    def __init__(self, air_handler, threshold):
        """
        @type air_handler: AirHandler
        """
        if air_handler is not AirHandler:
            raise ValueError("air_handler must be of type AirHandler")

        self.air_handler = air_handler
        self.AC = True # should we use the heater to attempt to keep heat in bounds?
        self.heater = True # should we we use the
        self.AC_target = -1
        self.heat_target = -1
        self.threshold = threshold # should be a temporary value, and should be replaced by an adaptive system

        Thermostat.thermostats.append(self) # we can't really mark a method so we will mark a class method


    def set_target(self, target_temp):
        """
        @type target_temp: int
        """
        self.AC_target = target_temp
        self.heat_target = target_temp

    def set_AC_target(self, target_temp):
        """
        @type target_temp: int
        """
        self.AC_target = target_temp

    def set_heat_target(self, target_temp):
        """
        @type target_temp: int
        """
        self.heat_target = target_temp


    def enable_AC(self, on):
        self.AC = on
        self.air_handler.set_AC(self.air_handler.AC_is_on() and on)

    def set_heater(self, on):
        self.heater = on
        self.air_handler.set_heater(self.air_handler.heater_is_on() and on)

    def set_fan(self, on):
        self.air_handler.set_heater(on)


    @staticmethod
    @temp_monitor.temp_changed
    def temp_changed(temp):
        for thermostat in Thermostat.thermostats:
            thermostat.temp_changed(temp)

    def manage(self, temp):
        if temp > self.AC_target:
            self.air_handler.set_AC(self.AC)
        elif temp < self.heat_target:
            self.air_handler.set_heater(self.heater)

        elif temp < (self.AC_target - self.threshold) and self.air_handler.AC_is_on():
            self.air_handler.set_AC(Off)
        elif temp > (self.heat_target + self.threshold) and self.air_handler.heater_is_on():
            self.air_handler.set_heater(Off)



