from flask import Flask
app = Flask(__name__)

import RPi.GPIO as GPIO
import smbus

on = False
bus = smbus.SMBus(1)

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)
GPIO.setup(27, GPIO.IN)

def read_temp(bus):
    return "temp is:" + str(bus.read_byte(0x48))


@app.route('/')
def toggle_relay():
    global on
    on = not on
    GPIO.output(4, on)
    return "On" if on else "Off"

@app.route('/temp')
def toggle_temp():
    global on
    return "On" if on else "Off"

app.run(host='0.0.0.0')



