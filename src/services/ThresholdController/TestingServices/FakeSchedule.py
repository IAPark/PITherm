from flask import Flask
from flask import json
from multiprocessing import Queue

responses_ = Queue()
port = 5001

app = Flask(__name__)


@app.route("/state/<int:time>")
def state(time: int):
    global responses_
    return json.jsonify(responses_.get())


def run(responses: Queue,):
    global responses_
    responses_ = responses
    app.run(port=port)
