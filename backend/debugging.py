from ticker import default_ticker
import services


def centigrade_to_fahrenheit(c):
    return c * 1.8000 + 32


@default_ticker.tick
def print_temp():
    print("temp: " + str(centigrade_to_fahrenheit(services.TempMonitor.last_temp)) + "(F), " +
          str(services.TempMonitor.last_temp))


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