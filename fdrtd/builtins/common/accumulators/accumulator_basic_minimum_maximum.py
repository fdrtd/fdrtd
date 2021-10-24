from fdrtd.builtins.common.accumulators.accumulator import Accumulator


class AccumulatorBasicMinimumMaximum(Accumulator):

    def __init__(self, _=None):
        self.samples = 0
        self.minimum = None
        self.maximum = None

    def serialize(self):
        return {'samples': self.samples,
                'minimum': self.minimum,
                'maximum': self.maximum}

    @staticmethod
    def deserialize(dictionary):
        accumulator = AccumulatorBasicMinimumMaximum
        accumulator.samples = dictionary['samples']
        accumulator.minimum = dictionary['minimum']
        accumulator.maximum = dictionary['maximum']
        return accumulator

    def add(self, other):
        self.samples = self.samples + other.samples
        self.minimum = min(self.minimum, other.minimum)
        self.maximum = max(self.maximum, other.maximum)

    def update(self, data):

        if self.samples == 0:
            self.samples = 1
            self.minimum = data['minimum']
            self.maximum = data['maximum']
            return

        self.samples = self.samples + 1
        self.minimum = min(self.minimum, data['minimum'])
        self.maximum = max(self.maximum, data['maximum'])

    def finalize(self):
        pass

    def get_samples(self):
        return self.samples

    def get_min(self):
        return self.minimum

    def get_max(self):
        return self.maximum
