__author__ = 'Isaac'
from multiprocessing.queues import Empty


class Router:
    def __init__(self):
        self.response_queue = None
        self.command_queue = None
        self.routes = {}

    def handle(self):
        try:
            command = self.command_queue.get(block=False)
            if command is not None:
                url = None
                try:
                    url = command["url"]
                    result = self[url](command["body"])
                    self.response_queue.put({"url": url, "body": result})
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