import math as _math
import sys as _sys

from fdrtd.builtins.common.accumulators.accumulator import Accumulator
from fdrtd.builtins.common.accumulators.accumulator_statistics_moments import AccumulatorStatisticsMoments


class AccumulatorStatisticsUnivariate(Accumulator):

    def __init__(self, _=None):
        self.moments = AccumulatorStatisticsMoments()
        self.samples = 0
        self.minimum = _sys.float_info.max
        self.maximum = _sys.float_info.min
        self.geometric = 0.0
        self.harmonic = 0.0

    def serialize(self):
        return {'moments': self.moments.serialize(),
                'samples': self.samples,
                'minimum': self.minimum,
                'maximum': self.maximum,
                'geometric': self.geometric,
                'harmonic': self.harmonic}

    @staticmethod
    def deserialize(dictionary):
        accumulator = AccumulatorStatisticsUnivariate()
        accumulator.moments = AccumulatorStatisticsMoments.deserialize(dictionary['moments'])
        accumulator.samples = dictionary['samples']
        accumulator.minimum = dictionary['minimum']
        accumulator.maximum = dictionary['maximum']
        accumulator.geometric = dictionary['geometric']
        accumulator.harmonic = dictionary['harmonic']
        return accumulator

    def add(self, other):
        self.moments.add(other.moments)
        self.samples += other.samples
        if self.minimum > other.minimum:
            self.minimum = other.minimum
        if self.maximum < other.maximum:
            self.maximum = other.maximum
        self.geometric += other.geometric
        self.harmonic += other.harmonic

    def update(self, data):
        self.moments.update(data)
        self.samples += 1
        if self.minimum > data:
            self.minimum = data
        if self.maximum < data:
            self.maximum = data
        if data > 0.0:
            self.geometric += _math.log(data)
        if data != 0.0:
            self.harmonic += 1.0 / data

    def finalize(self):
        self.moments.set_center(self.get_mean())

    def encrypt_data_for_upload(self, nonce, power=1):
        return {'moments': self.moments.encrypt_data_for_upload(nonce, power=power),
                'samples': self.samples,
                'minimum': nonce.encrypt_numerical(self.minimum, power=power),
                'maximum': nonce.encrypt_numerical(self.maximum, power=power),
                'geometric': self.geometric + _math.log(nonce.numerical) * power * self.samples,
                'harmonic': self.harmonic / pow(nonce.numerical, power)}

    @staticmethod
    def decrypt_result_from_download(encrypted, nonce):
        decryption_powers = {'minimum': 1, 'maximum': 1, 'sum': 1,
                             'mean': 1, 'harmonic_mean': 1, 'geometric_mean': 1,
                             'variance': 2, 'variance_mle': 2, 'variance_of_sample_mean': 2,
                             'standard_deviation': 1, 'standard_deviation_mle': 1, 'standard_error_of_sample_mean': 1,
                             'coefficient_of_variation': 0, 'coefficient_of_variation_mle': 0,
                             'root_mean_square': 1, 'root_mean_square_deviation': 1, 'skewness': 0,
                             'kurtosis': 0, 'kurtosis_excess': 0, 'hyper_skewness': 0, 'hyper_flatness': 0}
        return nonce.decrypt_dictionary_numerical(encrypted, decryption_powers)

    def calculate_raw_moment(self, k):
        if k == 0:
            return 1.0
        return self.moments.uncentered[k - 1] / self.samples

    def calculate_central_moment(self, k):
        if k == 0:
            return 1.0
        if k == 1:
            return 0.0
        return self.moments.centered[k - 1] / self.samples

    def calculate_standardized_moment(self, k):
        if k == 0:
            return 1.0
        return self.calculate_central_moment(k) * pow(self.get_variance_mle(), -0.5 * k)

    def calculate_raw_moments(self):
        return [self.calculate_raw_moment(k) for k in range(6)]

    def calculate_central_moments(self):
        return [self.calculate_central_moment(k) for k in range(6)]

    def calculate_standardized_moments(self):
        return [self.calculate_standardized_moment(k) for k in range(6)]

    def calculate_center(self):
        return self.moments.center
    
    @staticmethod
    def list_outputs():
        return ['samples', 'minimum', 'maximum', 'sum', 'mean', 'harmonic_mean', 'geometric_mean',
                'variance', 'variance_mle', 'variance_of_sample_mean', 'standard_deviation', 'standard_deviation_mle',
                'standard_error_of_sample_mean', 'coefficient_of_variation', 'coefficient_of_variation_mle',
                'root_mean_square', 'root_mean_square_deviation',
                'skewness', 'kurtosis', 'kurtosis_excess', 'hyper_skewness', 'hyper_flatness']

    def get_samples(self):
        return self.samples

    def get_minimum(self):
        return self.minimum

    def get_maximum(self):
        return self.maximum

    def get_sum(self):
        return self.moments.uncentered[0]

    def get_mean(self):
        return self.moments.uncentered[0] / self.samples

    def get_harmonic_mean(self):
        return self.samples / self.harmonic

    def get_geometric_mean(self):
        return _math.exp(self.geometric / self.samples)

    def get_variance(self):
        return self.moments.centered[1] / (self.samples - 1.0)

    def get_variance_mle(self):
        return self.moments.centered[1] / self.samples

    def get_variance_of_sample_mean(self):
        return self.get_variance() / self.samples

    def get_standard_deviation(self):
        return _math.sqrt(self.get_variance())

    def get_standard_deviation_mle(self):
        return _math.sqrt(self.get_variance_mle())

    def get_standard_error_of_sample_mean(self):
        return _math.sqrt(self.get_variance_of_sample_mean())

    def get_coefficient_of_variation(self):
        return self.get_standard_deviation() / self.get_mean()

    def get_coefficient_of_variation_mle(self):
        return self.get_standard_deviation_mle() / self.get_mean()

    def get_root_mean_square(self):
        return _math.sqrt(self.calculate_raw_moment(2))

    def get_root_mean_square_deviation(self):
        return _math.sqrt(self.calculate_central_moment(2))

    def get_skewness(self):
        return self.calculate_standardized_moment(3)

    def get_kurtosis(self):
        return self.calculate_standardized_moment(4)

    def get_kurtosis_excess(self):
        return self.get_kurtosis() - 3.0

    def get_hyper_skewness(self):
        return self.calculate_standardized_moment(5)

    def get_hyper_flatness(self):
        return self.calculate_standardized_moment(6)
