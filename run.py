import json

from bson import json_util
from flask import request, Response
from flask.ext.cors import CORS

from API import app
from database.temp_log import TempLog
from security import logged_in_route
from hardware_abstraction import Pin
from API_to_backend import response_queue, command_queue, start_backend, get_for
CORS(app)

print("run loaded")

@app.route('/temp')
def get_temp():
    command_queue.put({"url": "/temp", "body": 0})
    return Response(json.dumps({"data": str(get_for("/temp", response_queue, 5))}, default=json_util.default), mimetype='application/json')


@app.route('/temps')
def get_temps():
    return Response(json.dumps({"data": TempLog.get_all_dic()}, default=json_util.default), mimetype='application/json')


@app.route('/stop')
@logged_in_route
def stop():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return "shutting down"

if not app.debug or True:
    import logging
    file_handler = logging.FileHandler("log.txt")
    file_handler.setLevel(logging.DEBUG)
    app.logger.addHandler(file_handler)

start_backend()
app.run(host='0.0.0.0', debug=True)
Pin.cleanup()

