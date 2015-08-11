import RPi.GPIO as GPIO
from constants import *


class Pin:
    def __init__(self, pin_id):
        self.pin_id = pin_id
        self.state = Off
        GPIO.setmode(GPIO.BCM)

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

    @classmethod
    def cleanup(cls):
        GPIO.cleanup()
