class air_hander:
    def __init__(self, fan_pin, heater_pin, AC_pin):
        self.fan_pin = fan_pin
        self.heater_pin = heater_pin
        self.AC_pin = AC_pin
        print("init")

    def set_AC(self, on):
        print("setting AC: " + "on" if on else "off")

    def set_heater(self, on):
        print("setting heater: " + "on" if on else "off")

    def set_fan(self, on):
        print("setting fan: " + "on" if on else "off")
