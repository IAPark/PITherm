from flask import Flask
app = Flask(__name__)

import threading
import RPi.GPIO as GPIO
import time

on = False
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)
GPIO.setup(27, GPIO.IN)

@app.route('/')
def hello_world():
    global on
    on = not on
    return 'Hello World!'

def local():
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

t = threading.Thread(target=local())
t.daemon = True
t.run()
print("still working")
app.run(host='0.0.0.0')



