# Thermostat controls the AC, Heater, and Fan
from datetime import datetime

from services.air_handler import AirHandler
from services import Services
from constants import *

temp_monitor = Services.TempMonitor # should be set in any class that imports


class Thermostat:
    thermostats = []
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

        Thermostat.thermostats.append(self)  # we can't really mark a method so we will mark a class method


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


    @staticmethod
    @temp_monitor.temp_changed
    def temp_changed(temp):
        for thermostat in Thermostat.thermostats:
            thermostat.manage(temp)

    def manage(self, temp):
        if (not self.AC_target is not None) or (not self.heat_target is not None):
            raise ValueError('AC_target and heat_target')

        if temp > self.AC_target:
            self.air_handler.set_AC(self.AC)
        elif temp < self.heat_target:
            self.air_handler.set_heater(self.heater)

        if temp < (self.AC_target - self.threshold):
            self.air_handler.set_AC(Off)
        if temp > (self.heat_target + self.threshold):
            self.air_handler.set_heater(Off)


    def tick(self, now):
        db = Services.DB
        scheduled = db.get_scheduled_state(now)

        if scheduled is None:
            state = db.get_repeating_change(now)["state"]
        else:
            state = scheduled["state"]

        self.set_AC_target(state["AC_target"])
        self.set_fan(state["fan"])
        self.set_heater_target(state["heater_target"])


