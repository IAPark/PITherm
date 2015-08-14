class Ticker:
    def __init__(self):
        self.to_run = []

    def tick(self, function):
        self.to_run.append(function)
        return function

    def tick_all(self):
        for function in self.to_run:
            function()


default_ticker = Ticker()
