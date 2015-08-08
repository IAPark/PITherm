import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)
GPIO.setup(27, GPIO.INPUT)

try:
    while not GPIO.input(27):
        GPIO.output(4, False)
        print("off")
        time.sleep(2)
        GPIO.output(4, True)
        print("on")
        time.sleep(2)
finally:
    GPIO.cleanup()


