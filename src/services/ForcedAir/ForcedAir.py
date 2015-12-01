import argparse

from flask import Flask
from src.pin import OutputPin

parser = argparse.ArgumentParser(description='Controls an AC System')
parser.add_argument("-p", "--port", type=int, help="the port to run server on", default=5003)
parser.add_argument("-a", "--AC_pin", type=int, help="the pin to turn on to activate the AC system", default=4)
parser.add_argument("--heater_pin", type=int, help="the pin to turn on to activate the heater", default=5)
parser.add_argument("-f", "--fan_pin", type=int, help="the pin to turn on to activate the fan", default=6)


args = parser.parse_args()

if args.AC_pin:
    AC_pin = OutputPin(args.AC_pin)
if args.heater_pin:
    heater_pin = OutputPin(args.heater_pin)
if args.fan_pin:
    fan_pin = OutputPin(args.fan_pin)


app = Flask(__name__)


@app.route("/ac/<on_off>", methods=["POST", "GET"])
def ac(on_off):
    on = on_off == 'on'
    AC_pin.set(on)
    return on_off


@app.route("/heater/<on_off>", methods=["POST", "GET"])
def heater(on_off):
    on = on_off == 'on'
    heater_pin.set(on)
    return on_off


@app.route("/fan/<on_off>", methods=["POST", "GET"])
def fan(on_off):
    on = on_off == 'on'
    fan_pin.set(on)
    return on_off

if __name__ == "__main__":
    app.run(debug=True, port=args.port)
