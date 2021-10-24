import math as _math

from fdrtd.builtins.common.accumulators.accumulator import Accumulator
from fdrtd.builtins.common.accumulators.accumulator_statistics_univariate import AccumulatorStatisticsUnivariate


class AccumulatorStatisticsBivariate(Accumulator):

    def __init__(self, _=None):
        self.accumulator_x = AccumulatorStatisticsUnivariate()
        self.accumulator_y = AccumulatorStatisticsUnivariate()
        self.accumulator_xy = AccumulatorStatisticsUnivariate()

    def serialize(self):
        return {'accumulator_x': self.accumulator_x.serialize(),
                'accumulator_y': self.accumulator_y.serialize(),
                'accumulator_xy': self.accumulator_xy.serialize()}

    @staticmethod
    def deserialize(dictionary):
        accumulator = AccumulatorStatisticsBivariate()
        accumulator.accumulator_x = AccumulatorStatisticsUnivariate.deserialize(dictionary['accumulator_x'])
        accumulator.accumulator_y = AccumulatorStatisticsUnivariate.deserialize(dictionary['accumulator_y'])
        accumulator.accumulator_xy = AccumulatorStatisticsUnivariate.deserialize(dictionary['accumulator_xy'])
        return accumulator

    def add(self, other):
        self.accumulator_x.add(other.accumulator_x)
        self.accumulator_y.add(other.accumulator_y)
        self.accumulator_xy.add(other.accumulator_xy)

    def update(self, data):
        (x, y) = data
        self.accumulator_x.update(x)
        self.accumulator_y.update(y)
        self.accumulator_xy.update(x*y)

    def finalize(self):
        self.accumulator_x.finalize()
        self.accumulator_y.finalize()
        self.accumulator_xy.finalize()

    def encrypt_data_for_upload(self, nonce):
        return {'accumulator_x': self.accumulator_x.encrypt_data_for_upload(nonce),
                'accumulator_y': self.accumulator_y.encrypt_data_for_upload(nonce),
                'accumulator_xy': self.accumulator_xy.encrypt_data_for_upload(nonce, power=2)}

    @staticmethod
    def decrypt_result_from_download(encrypted, nonce):
        decryption_powers = {'samples': 0, 'covariance_mle': 2, 'covariance': 2, 'correlation_coefficient': 0,
                             'regression_slope': 0, 'regression_interceipt': 1, 'regression_slope_only': 0}
        return nonce.decrypt_dictionary_numerical(encrypted, decryption_powers)

    def get_samples(self):
        return self.accumulator_xy.get_samples()

    def get_covariance_mle(self):
        return self.accumulator_xy.get_mean() - self.accumulator_x.get_mean() * self.accumulator_y.get_mean()

    def get_covariance(self):
        return self.get_covariance_mle() / (1.0 - 1.0 / self.accumulator_xy.get_samples())

    def get_correlation_coefficient(self):
        return self.get_covariance() / _math.sqrt(self.accumulator_x.get_variance() * self.accumulator_y.get_variance())

    def get_regression_slope(self):
        return self.get_covariance() / self.accumulator_x.get_variance()

    def get_regression_interceipt(self):
        return self.accumulator_y.get_mean() - self.get_regression_slope() * self.accumulator_x.get_mean()

    def get_regression_slope_only(self):
        return self.accumulator_xy.get_mean() / self.accumulator_x.calculate_raw_moment(2)
