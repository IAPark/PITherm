from src.services.monolithic.services import default_ticker


class TempMonitor:
    def __init__(self, temperature_sensor):
        self.temperature_sensor = temperature_sensor
        self.temperature_changed_listeners = []
        self.last_temp = None # any real temperature should be different

        @default_ticker.tick
        def tick():
            self.check_temp()

    def check_temp(self):
        temp = self.temperature_sensor.get_temp()

        if temp != self.last_temp:
            for listener in self.temperature_changed_listeners:
                listener(temp)

        self.last_temp = temp

    def temp_changed(self, function):
        """
        A simple decorator to designed to record listeners to be called when temperature changes

        :param function: The function to record must take as first and only argument a number as the temperature
        :return: function
        """

        self.temperature_changed_listeners.append(function)
        return function


