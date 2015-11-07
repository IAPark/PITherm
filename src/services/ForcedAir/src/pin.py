import RPi.GPIO as GPIO


class Pin:
    pins = 0 # the total number of pins in use Pins will be cleaned up when pins <= 0

    def __init__(self, pin_id):
        self.pin_id = pin_id
        self.state = True
        GPIO.setmode(GPIO.BCM)
        self.pins += 1

    def __del__(self):
        self.pins -= 1
        if self.pins <= 0:
            GPIO.cleanup()

    def sense(self):
        GPIO.setup(self.pin_id, GPIO.IN)
        output = GPIO.input(self.pin_id)
        self.state = output
        return output

    def set(self, state):
        GPIO.setup(self.pin_id, GPIO.OUT)
        GPIO.output(self.pin_id, state)
        self.state = state

    def get(self):
        return self.state


class InputPin(Pin):
    def __init__(self, pin_id):
        super().__init__(pin_id)
        GPIO.setup(self.pin_id, GPIO.IN)

    def sense(self):
        output = GPIO.input(self.pin_id)
        self.state = output
        return output

    def set(self, state):
        self.state = state

    def get(self):
        return self.state


class OutputPin(Pin):
    def __init__(self, pin_id):
        super().__init__(pin_id)
        GPIO.setup(self.pin_id, GPIO.OUT)

    def sense(self):
        return self.state

    def set(self, state):
        GPIO.output(self.pin_id, state)
        self.state = state

    def get(self):
        return self.state

