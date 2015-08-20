import json

from bson import json_util
from flask import request

from API import app
from security import logged_in_route
from hardware_abstraction import Pin
from API_to_backend import response_queue, command_queue, start_backend, get_for
import ssl

context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain('ia.crt', 'ia.key')

@app.route('/temp')
@logged_in_route
def get_temp():
    command_queue.put({"url": "/temp", "body": 0})
    return str(get_for("/temp", response_queue, 5))


@app.route('/temps')
@logged_in_route
def get_temps():
    command_queue.put({"url": "/temps", "body": 0})
    return json.dumps({"data": get_for("/temps", response_queue, 5)}, default=json_util.default)


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
app.run(host='0.0.0.0', debug=True, ssl_context=context)
Pin.cleanup()

