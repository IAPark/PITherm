__author__ = 'Isaac'
from multiprocessing.queues import Empty


class Router:
    def __init__(self, response_queue, command_queue):
        self.response_queue = response_queue
        self.command_queue = command_queue
        self.routes = {}

    def handle(self):
        try:
            command = self.command_queue.get(block=False)
            if command is not None:
                url = None
                try:
                    url = command["url"]
                    self.response_queue.put({"url": url, "body": self[url](command["body"])})
                except KeyError:
                    print("could not handle " + str(url))
        except Empty:
            pass

    def route(self, url):
        def decorator(function):
            self.routes[url] = function
            return function
        return decorator

    def __getitem__(self, item):
        return self.routes[item]