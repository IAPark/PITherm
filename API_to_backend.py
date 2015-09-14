from multiprocessing import Queue, Process
import time
import backend
command_queue = Queue()
response_queue = Queue()


def start_backend():
    if handler:
        handler.stop()
    handler = Process(target=backend.start, args=(command_queue, response_queue))
    handler.start()


def get_for(url, queue, timeout):
    beginning = time.time()
    result = queue.get(timeout=timeout)
    if result["url"] == url:
        return result["body"]
    else:
        queue.put(result)
        return get_for(url, queue, timeout - (time.time()-beginning))