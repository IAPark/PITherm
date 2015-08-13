import smbus


class TemperatureSensor:
    def __init__(self, address):
        self.bus = smbus.SMBus(1)
        self.address = address

    def get_temp(self):
        return self.bus.readByte(self.address)