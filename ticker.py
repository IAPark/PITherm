from heapq import heappush, heappop, heapreplace


class Ticker:
    def __init__(self):
        self.to_run = []
        self.tick = 0
        self.index = 0

    def tick(self, function):
        self.to_run.append(function)
        return function

    def tick_all(self):
        for function in self.to_run:
            function()


default_ticker = Ticker()
