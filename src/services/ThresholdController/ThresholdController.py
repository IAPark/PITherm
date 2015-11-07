import argparse

import time
from flask import Flask, request
import requests

parser = argparse.ArgumentParser(description='Control temperature based on a threshold'
                                             ' above or below which the system reacts')
parser.add_argument("AC_system_url", help="the url of the AC_system to use")
parser.add_argument("state_provider_url", help="the url of the State Provider to use")
parser.add_argument("threshold", default=3, type=float, help="the threshold to use")
parser.add_argument("-p", "--port", type=int, help="the port to run server on", default=5000)
args = parser.parse_args()

app = Flask(__name__)


def get_state():
    state = requests.get(args.state_provider_url + "/state/"+str(int(time.time())))
    return state.json()


def set_heater(on: bool):
    requests.post(args.AC_system_url + "/heater/" + ("on" if on else "off"))


def set_AC(on: bool):
    requests.post(args.AC_system_url + "/ac/" + ("on" if on else "off"))


@app.route("/temp", methods=["POST"])
def temp_changed():
    temp = request.get_json()["temp"]
    state = get_state()

    if state["AC_target"] + args.threshold < temp:
        set_AC(True)
        return "cooling"

    elif state["heat_target"] - args.threshold > temp:
        set_heater(True)
        return "heating"

    elif state["AC_target"] > temp > state["heat_target"]:
        set_heater(False)
        set_AC(False)
        return "holding"
    return "in threshold"


if __name__ == "__main__":
    app.run(debug=True, port=args.port)