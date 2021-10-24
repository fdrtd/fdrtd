from fdrtd.builtins.common.accumulators.accumulator import Accumulator


class AccumulatorStatisticsMoments(Accumulator):

    def __init__(self, _=None):
        self.samples = 0
        self.center = 0.0
        self.uncentered = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.centered = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    def serialize(self):
        return {'samples': self.samples,
                'center': self.center,
                'uncentered': self.uncentered,
                'centered': self.centered}

    @staticmethod
    def deserialize(dictionary):
        accumulator = AccumulatorStatisticsMoments()
        accumulator.samples = dictionary['samples']
        accumulator.center = dictionary['center']
        accumulator.uncentered = dictionary['uncentered']
        accumulator.centered = dictionary['centered']
        return accumulator

    def add(self, other):

        if self.samples == 0:
            self.center = other.center

        self.samples += other.samples

        for k in range(6):
            self.uncentered[k] += other.uncentered[k]
            self.centered[k] += other.recenter(k, self.center)

    def update(self, datum):

        if self.samples == 0:
            self.center = datum

        self.samples = self.samples + 1

        temp = datum
        temp2 = temp * temp
        temp3 = temp2 * temp

        self.uncentered[0] += temp
        self.uncentered[1] += temp2
        self.uncentered[2] += temp3
        self.uncentered[3] += temp2 * temp2
        self.uncentered[4] += temp2 * temp3
        self.uncentered[5] += temp3 * temp3

        temp = datum - self.center
        temp2 = temp * temp
        temp3 = temp2 * temp

        self.centered[0] += temp
        self.centered[1] += temp2
        self.centered[2] += temp3
        self.centered[3] += temp2 * temp2
        self.centered[4] += temp2 * temp3
        self.centered[5] += temp3 * temp3

    def encrypt_data_for_upload(self, nonce, power=1):
        uncentered = [nonce.encrypt_numerical(self.uncentered[i], power=(i+1)*power) for i in range(6)]
        centered = [nonce.encrypt_numerical(self.centered[i], power=(i+1)*power) for i in range(6)]
        return {'samples': self.samples,
                'center': nonce.encrypt_numerical(self.center, power=power),
                'uncentered': uncentered,
                'centered': centered}

    def set_center(self, center):
        recentered = [self.recenter(k, center) for k in range(6)]
        self.centered = recentered
        self.center = center

    def recenter(self, k, center):
        pascal = [[1.0], [1.0, 1.0], [1.0, 2.0, 1.0], [1.0, 3.0, 3.0, 1.0], [1.0, 4.0, 6.0, 4.0, 1.0],
                  [1.0, 5.0, 10.0, 10.0, 5.0, 1.0], [1.0, 6.0, 15.0, 20.0, 15.0, 6.0, 1.0]]

        recentered = pow(self.center - center, k + 1) * self.samples
        for j in range(k + 1):
            recentered += self.centered[k - j] * (pascal[k + 1][j] * pow(self.center - center, j))

        return recentered

    def get_samples(self):
        return self.samples

    def get_center(self):
        return self.center

    def get_uncentered(self, k):
        return self.uncentered[k]

    def get_centered(self, k):
        return self.centered[k]
