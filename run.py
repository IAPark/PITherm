from flask import Flask
from flask import request
app = Flask(__name__)

import RPi.GPIO as GPIO
import smbus

on = False
bus = smbus.SMBus(1)

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)
GPIO.setup(27, GPIO.IN)

def read_temp(bus):
    return bus.read_byte(0x48)


@app.route('/')
def toggle_relay():
    global on
    on = not on
    GPIO.output(4, on)
    return "On" if on else "Off"

@app.route('/temp')
def read_temp():
    global bus
    return "temp is:" + str(read_temp(bus))

@app.route('/stop')
def stop():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return "shutting down"

app.run(host='0.0.0.0')



