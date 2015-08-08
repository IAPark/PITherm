from flask import Flask
app = Flask(__name__)

import RPi.GPIO as GPIO
import time

on = False;

@app.route('/')
def hello_world():
    global on
    on = not on
    return 'Hello World!'

if __name__ == '__main__':
    app.run()

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)
GPIO.setup(27, GPIO.IN)

try:
    while not GPIO.input(27):
        GPIO.output(4, False)
        print("off")
        time.sleep(2)
        GPIO.output(4, on)
        print("on")
        time.sleep(2)
finally:
    GPIO.cleanup()


