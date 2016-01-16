import argparse

import time
from flask import Flask
from src.pin import OutputPin

lockout = 0
AC_pin_number = None
heater_pin_number = None
fan_pin_number = None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Controls an AC System')
    parser.add_argument("-p", "--port", type=int, help="the port to run server on", default=5003)
    parser.add_argument("-a", "--AC_pin", type=int, help="the pin to turn on to activate the AC system", default=4)
    parser.add_argument("-e", "--heater_pin", type=int, help="the pin to turn on to activate the heater", default=5)
    parser.add_argument("-f", "--fan_pin", type=int, help="the pin to turn on to activate the fan", default=6)
    parser.add_argument("-l", "--lockout", type=int, help="a period after any changes in seconds in which no changes can be made", default=120)

    args = parser.parse_args()

    lockout = args.lockout
    AC_pin_number = args.AC_pin
    heater_pin_number = args.heater_pin
    fan_pin_number = args.fan_pin

if AC_pin_number:
    AC_pin = OutputPin(AC_pin_number)
if heater_pin_number:
    heater_pin = OutputPin(heater_pin_number)
if fan_pin_number:
    fan_pin = OutputPin(fan_pin_number)

app = Flask(__name__)
app.debug = True

ac = False
heater = False
fan = False
last_change = 0


@app.route("/ac/<on_off>", methods=["POST", "GET"])
def ac(on_off):
    global ac, last_change
    old = ac
    ac = on_off == 'on'
    if heater_pin.get() and ac:
        app.logger.error("Attempted to to turn ac on while heater was running")
        ac = False
        return "error: heater on"

    if time.time() - last_change < lockout and old != ac:
        ac = old

    AC_pin.set(ac)
    last_change = time.time()
    return "True" if ac else "False"


@app.route("/heater/<on_off>", methods=["POST", "GET"])
def heater(on_off):
    global heater, ac, last_change
    old = heater

    heater = on_off == 'on'
    if AC_pin.get() and heater:
        app.logger.error("Attempted to to turn heater on while ac was running")
        heater = False
        return "error: AC on"

    if time.time() - last_change < lockout and old != heater:
        heater = old

    heater_pin.set(heater)
    last_change = time.time()
    return "True" if heater else "False"


@app.route("/fan/<on_off>", methods=["POST", "GET"])
def fan(on_off):
    global fan
    fan = on_off == 'on'
    fan_pin.set(fan)
    return "True" if fan else "False"

if __name__ == "__main__":
    app.run(debug=True, port=args.port, host='0.0.0.0')
