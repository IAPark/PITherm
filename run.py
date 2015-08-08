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
    GPIO.output(4, on)

app.run(host='0.0.0.0')



