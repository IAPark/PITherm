from flask import Flask
from flask import request
from hardware_abstraction.pin import Pin
from multiprocessing import Queue, Process
from backend.backend import start
app = Flask(__name__)

command_queue = Queue()
response_queue = Queue()
handler = Process(target=start, args=(command_queue, response_queue,))
handler.start()
@app.route('/temp')
def print_temp():
    command_queue.put({"url": "/temp", "body": 0})
    return response_queue.get()

@app.route('/stop')
def stop():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return "shutting down"

app.run(host='0.0.0.0', debug=True)
Pin.cleanup()

