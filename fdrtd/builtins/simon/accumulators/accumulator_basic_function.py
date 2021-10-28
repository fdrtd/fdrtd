from fdrtd.builtins.simon.accumulators.accumulator import Accumulator


class AccumulatorBasicFunction(Accumulator):

    def __init__(self, initial, function):
        self.samples = 0
        self.data = initial
        self.function = function

    def add(self, other):
        self.samples = self.samples + other.samples
        self.data = self.function(self.data, other.data)

    def update(self, data):
        if isinstance(data, list):
            self.samples = self.samples + len(data)
            for datum in data:
                self.data = self.function(self.data, datum)
        else:
            self.samples = self.samples + 1
            self.data = self.function(self.data, data)

    def finalize(self):
        pass

    def get_samples(self):
        return self.samples

    def get_data(self):
        return self.data
