from flask import Flask
from multiprocessing import Queue

port = 5000
responses_ = Queue()

app = Flask(__name__)


@app.route("/ac/<on_off>")
def ac(on_off: str):
    global responses_
    responses_.put({"ac": on_off})


@app.route("/heater/<on_off>")
def heater(on_off: str):
    global responses_
    responses_.put({"heater": on_off})


@app.route("/fan/<on_off>")
def fan(on_off: str):
    global responses_
    responses_.put({"fan": on_off})



def run(responses: Queue,):
    global responses_
    responses_ = responses
    app.run(port=port)
