import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)

try:
    while True:
        GPIO.output(4, False)
        print("off")
        time.sleep(2)
        GPIO.output(4, True)
        print("on")
        time.sleep(2)
except:
    GPIO.cleanup()


