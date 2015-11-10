import smbus


class TemperatureSensor:
    temp_history = []
    last_temp = 0

    def __init__(self, address):
        self.bus = smbus.SMBus(1)
        self.address = address

    def get_temp(self):
        MSB = self.bus.read_byte_data(self.address, 0)
        LSB = self.bus.read_byte_data(self.address, 1)

        temp = ((MSB << 8 | LSB) >> 4) * 0.0625
        result = temp

        # smooth the data slightly
        history_length = 3

        for t in self.temp_history:
            if abs(t - temp) > 0.2:
                result = self.last_temp
                break

        self.temp_history.append(temp)
        self.temp_history = self.temp_history[0:history_length]
        self.last_temp = result

        return result