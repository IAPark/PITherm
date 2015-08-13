from API import app
from security import logged_in_route
from hardware_abstraction.pin import Pin
from API_to_backend import response_queue, command_queue, start_backend, get_for
from bson import json_util
import json


@app.route('/temp')
@logged_in_route
def get_temp():
    command_queue.put({"url": "/temp", "body": 0})
    return str(get_for("/temp", response_queue, 5))


@app.route('/temps')
def get_temps():
    command_queue.put({"url": "/temps", "body": 0})
    return json.dumps({"data": get_for("/temps", response_queue, 5)}, default=json_util.default)

start_backend()
app.run(host='0.0.0.0', debug=True)
Pin.cleanup()

