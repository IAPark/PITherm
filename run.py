import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)

while True:
    GPIO.output(4, False)
    time.sleep(2)
    GPIO.output(4, True)

