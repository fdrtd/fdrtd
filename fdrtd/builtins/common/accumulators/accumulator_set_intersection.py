from fdrtd.builtins.common.accumulators.accumulator import Accumulator


class AccumulatorSetIntersection(Accumulator):

    def __init__(self, _=None):
        self.samples = 0
        self.set = set()

    def serialize(self):
        return {'samples': self.samples,
                'set': list(self.set)}

    @staticmethod
    def deserialize(dictionary):
        accumulator = AccumulatorSetIntersection()
        accumulator.samples = dictionary['samples']
        accumulator.set = set(dictionary['set'])
        return accumulator

    def add(self, other):
        if self.samples == 0:
            self.set = other.set
        else:
            self.set = self.set.intersection(other.set)
        self.samples = self.samples + other.samples

    def update(self, data):
        if self.samples == 0:
            self.set = set(data)
        else:
            self.set = self.set.intersection(set(data))
        self.samples = self.samples + 1

    def finalize(self):
        pass

    def get_samples(self):
        return self.samples

    def get_size_intersection(self):
        return len(self.set)

    def get_intersection(self):
        return list(self.set)
