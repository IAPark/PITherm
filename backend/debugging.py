import services


def centigrade_to_fahrenheit(c):
    return c * 1.8000 + 32


@services.TempMonitor.temp_changed
def print_temp(temp):
    print("temp: " + str(centigrade_to_fahrenheit(temp)) + "(F), " +
          str(temp))


class FakePin:

    def __init__(self, name):
        self.name = name
        self.state = False

    def sense(self):
        return False

    def set(self, state):
        self.state = state


    def get(self):
        return self.state