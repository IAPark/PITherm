__author__ = 'Isaac'


class Router:
    def __init__(self):
        self.routes = {}

    def route(self, url):
        def decorator(function):
            self.routes[url] = function
            return function

    def __getitem__(self, item):
        return self.routes[item]