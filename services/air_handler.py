from database.state_log import StateLog

class AirHandler:
    def __init__(self, fan_pin, heater_pin, AC_pin):
        self.fan_pin = fan_pin
        self.heater_pin = heater_pin
        self.AC_pin = AC_pin

    def set_AC(self, on):
        self.AC_pin.set(on)
        StateLog(self.AC_pin.get(), self.heater_pin.get(), self.fan_pin.get()).save()

    def AC_is_on(self):
        return self.AC_pin.get()

    def set_heater(self, on):
        self.heater_pin.set(on)
        StateLog(self.AC_pin.get(), self.heater_pin.get(), self.fan_pin.get()).save()

    def heater_is_on(self):
        return self.heater_pin.get()

    def set_fan(self, on):
        self.fan_pin.set(on)
        StateLog(self.AC_pin.get(), self.heater_pin.get(), self.fan_pin.get()).save()

    def fan_is_on(self):
        return self.fan_pin.get()
