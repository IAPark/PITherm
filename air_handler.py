from pin import Pin


class AirHandler:
    def __init__(self, fan_pin, heater_pin, AC_pin):
        """
        @type fan_pin:  Pin
        @type heater_pin: Pin
        @type AC_pin: Pin
        """
        self.fan_pin = fan_pin
        self.heater_pin = heater_pin
        self.AC_pin = AC_pin
        print("init")

    def set_AC(self, on):
        self.AC_pin.set(on)
        print("setting AC: " + "on" if on else "off")

    def AC_is_on(self):
        return self.AC_pin.get()

    def set_heater(self, on):
        self.heater_pin.set(on)
        print("setting heater: " + "on" if on else "off")

    def heater_is_on(self):
        return self.heater_pin.get()

    def set_fan(self, on):
        self.fan_pin.set(on)
        print("setting fan: " + "on" if on else "off")

    def fan_is_on(self):
        return self.fan_pin.get()
