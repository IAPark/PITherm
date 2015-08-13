from flask import Flask
from flask import request
from hardware_abstraction.pin import Pin
from multiprocessing import Queue, Process
from backend.backend import start
from bson import json_util
import json
import time
from security import logged_in_route

app = Flask(__name__)

command_queue = Queue()
response_queue = Queue()
handler = Process(target=start, args=(command_queue, response_queue,))
handler.start()


def get_for(url, queue, timeout):
    beginning = time.time()
    result = queue.get(timeout=timeout)
    if result["url"] == url:
        return result["body"]
    else:
        queue.put(result)
        return get_for(url, queue, timeout - (time.time()-beginning))


@app.route('/temp')
@logged_in_route
def get_temp():
    command_queue.put({"url": "/temp", "body": 0})
    return str(get_for("/temp", response_queue, 5))


@app.route('/temps')
def get_temps():
    command_queue.put({"url": "/temps", "body": 0})
    return json.dumps({"data": get_for("/temps", response_queue, 5)}, default=json_util.default)



# Routes to modify the repeating schedule
@app.route('/schedule/repeating', methods=["GET"])
def get_repeating_schedule():
    command_queue.put({"url": "/schedule/repeating/GET", "body": 0})
    return json.dumps({"data": get_for("/schedule/repeating/GET", response_queue, 5)}, default=json_util.default)


@app.route('/schedule/repeating', methods=["POST"])
@logged_in_route
def add_repeating_schedule():
    command_queue.put({"url": "/schedule/repeating/POST", "body": request.get_json()})
    return json.dumps({"data": get_for("/schedule/repeating/POST", response_queue, 5)}, default=json_util.default)


@app.route('/schedule/repeating', methods=["DELETE"])
@logged_in_route
def remove_repeating_schedule():
    command_queue.put({"url": "/schedule/repeating/DELETE", "body": request.get_json()})
    return json.dumps({"data": get_for("/schedule/repeating/DELETE", response_queue, 5)}, default=json_util.default)



# Routes to modify the non repeating schedule
@app.route('/schedule', methods=["GET"])
@logged_in_route
def get_schedule():
    command_queue.put({"url": "/schedule/GET", "body": 0})
    return json.dumps({"data": get_for("/schedule/GET", response_queue, 5)}, default=json_util.default)


@app.route('/schedule', methods=["POST"])
@logged_in_route
def add_schedule():
    command_queue.put({"url": "/schedule/POST", "body": request.get_json()})
    return json.dumps({"data": get_for("/schedule/POST", response_queue, 5)}, default=json_util.default)


@app.route('/schedule', methods=["DELETE"])
@logged_in_route
def remove_schedule():
    command_queue.put({"url": "/schedule/DELETE", "body": request.get_json()})
    return json.dumps({"data": get_for("/schedule/DELETE", response_queue, 5)}, default=json_util.default)

@app.route('/stop')
@logged_in_route
def stop():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return "shutting down"

app.run(host='0.0.0.0', debug=True)
Pin.cleanup()

