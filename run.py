import RPi.GPIO as GPIO
import time

# assumes we only do this from one program
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)

try:
    while True:
        GPIO.output(4, False)
        print("off")
        time.sleep(2)
        GPIO.output(4, True)
        print("on")
except:
    GPIO.cleanup()


