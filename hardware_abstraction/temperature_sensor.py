import smbus


class TemperatureSensor:
    temp_history = []

    def __init__(self, address):
        self.bus = smbus.SMBus(1)
        self.address = address

    def get_temp(self):
        MSB = self.bus.read_byte_data(self.address, 0)
        LSB = self.bus.read_byte_data(self.address, 1)

        temp = ((MSB << 8 | LSB) >> 4) * 0.0625
        result = temp

        # smooth the data slightly
        if len(self.temp_history) > 0:
            if self.temp_history[0] - temp < 0.3:
                if len(self.temp_history) > 1:
                    if self.temp_history[1] - temp < 0.3:
                        if len(self.temp_history) > 2:
                            if not self.temp_history[2] - temp < 0.3:
                                result = self.temp_history[2]
                    else:
                        result = self.temp_history[0]
            else:
                result = self.temp_history[0]

        self.temp_history.append(temp)
        self.temp_history = self.temp_history[0:3]

        return result