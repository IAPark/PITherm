# Thermostat controls the AC, Heater, and Fan

import services
from constants import *
from database.state_change import StateChange
from database.state_change_repeating import StateChangeRepeating


class Thermostat:
    def __init__(self, air_handler, threshold):
        """
        @type air_handler: AirHandler
        """

        self.air_handler = air_handler
        self.AC = False  # should we use the heater to attempt to keep heat in bounds?
        self.heater = False
        self.AC_target = None
        self.heat_target = None
        self.threshold = threshold  # should be a temporary value, and should be replaced by an adaptive system

        @services.TempMonitor.temp_changed
        def temp_changed(temp):
            self.manage(temp)


    def set_target(self, target_temp):
        """
        @type target_temp: int
        """
        self.AC_target = target_temp + self.threshold
        self.heat_target = target_temp - self.threshold

    def set_AC_target(self, target_temp):
        """
        @type target_temp: int
        """
        self.AC_target = target_temp

    def set_heater_target(self, target_temp):
        """
        @type target_temp: int
        """
        self.heat_target = target_temp

    def enable_AC(self, on):
        self.AC = on
        self.air_handler.set_AC(self.air_handler.AC_is_on() and on)

    def enable_heater(self, on):
        self.heater = on
        self.air_handler.set_heater(self.air_handler.heater_is_on() and on)

    def set_fan(self, on):
        self.air_handler.set_heater(on)

    def manage(self, temp):
        if (not self.AC_target is not None and self.AC) or (not self.heat_target is not None and self.heater):
            raise ValueError('AC_target and heat_target')

        if self.AC and temp > self.AC_target:
            self.air_handler.set_AC(self.AC)
        elif self.heater and temp < self.heat_target:
            self.air_handler.set_heater(self.heater)

        if not self.AC or temp < (self.AC_target - self.threshold):
            self.air_handler.set_AC(Off)
        if not self.heater or temp > (self.heat_target + self.threshold):
            self.air_handler.set_heater(Off)


    def tick(self, now):
        scheduled = StateChange.get_current(now)

        if scheduled is None:
            scheduled = StateChangeRepeating.get_current(now)

        self.set_AC_target(scheduled.AC_target)
        self.set_fan(scheduled.fan)
        self.set_heater_target(scheduled.heater_target)


