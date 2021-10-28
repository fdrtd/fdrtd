from fdrtd.builtins.simon.accumulators.accumulator import Accumulator


class AccumulatorStatisticsFrequency(Accumulator):

    def __init__(self, _=None):
        self.samples = 0
        self.histogram = {}
        self.mode = None

    def serialize(self):
        return {'samples': self.samples,
                'mode': self.mode,
                'histogram': self.histogram}

    @staticmethod
    def deserialize(dictionary):
        accumulator = AccumulatorStatisticsFrequency()
        accumulator.samples = dictionary['samples']
        accumulator.mode = dictionary['mode']
        accumulator.histogram = dictionary['histogram']
        return accumulator

    def add(self, other):
        self.samples += other.samples
        for item in other.histogram:
            self.histogram[item] = self.histogram.get(item, 0) + other.histogram[item]

    def update(self, key, value=1):
        self.samples = self.samples + value
        self.histogram[key] = self.histogram.get(key, 0) + value

    def finalize(self):
        maximum = 0
        for item in self.histogram:
            if self.histogram[item] > maximum:
                maximum = self.histogram[item]
                self.mode = item

    def get_histogram(self):
        return self.histogram

    def get_samples(self):
        return self.samples

    def get_mode(self):
        return self.mode
