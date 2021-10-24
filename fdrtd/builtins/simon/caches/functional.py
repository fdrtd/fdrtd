from fdrtd.builtins.simon.caches.cache import Cache


class CacheFunctional(Cache):

    def __init__(self, function, minimum=1, maximum=-1):
        super().__init__()
        self.function = function
        self.intermediate = None
        self.count = 0
        self.minimum = minimum
        self.maximum = maximum

    def process(self, data):
        if self.count < self.maximum or self.maximum == -1:
            if self.intermediate is None:
                self.intermediate = data
            else:
                self.intermediate = self.function(self.intermediate, data)
            self.count = self.count + 1
        if self.count >= self.minimum:
            self.data = self.intermediate
