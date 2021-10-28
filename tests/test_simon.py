from tests.api import TestApi
from tests.assertions import TestAssertions
from tests.interface import TestInterface


class TestSimon(TestAssertions):

    def test_basic_sum(self):
        self.run_two_party_test(microprotocol='BasicSum',
                                data_alice=123.456789,
                                data_bob=1234.56789,
                                correct={'sum': 1358.024679})

    def test_basic_sum_3p(self):
        self.run_three_party_test(microprotocol='BasicSum',
                                  data_alice=123.456789,
                                  data_bob=1234.56789,
                                  data_charlie=12345.6789,
                                  correct={'sum': 13703.703579})

    def test_set_intersection(self):
        self.run_two_party_test(microprotocol='SetIntersection',
                                data_alice=[['A', 'B', 'C', 'D', 'E', 'F', 'G'],
                                            ['E', 'C', 'B', 'A', 'D']],
                                data_bob=[['C', 'F', 'A'], ['C', 'F', 'A', 'D']],
                                correct={'samples': 4,
                                         'size_intersection': 2,
                                         'intersection': ['A', 'C']})

    def test_set_intersection_size(self):
        self.run_two_party_test(microprotocol='SetIntersectionSize',
                                data_alice=[['A', 'B', 'C', 'D', 'E', 'F', 'G'],
                                            ['E', 'C', 'B', 'A', 'D']],
                                data_bob=[['C', 'F', 'A'], ['C', 'F', 'A', 'D']],
                                correct={'samples': 4, 'size_intersection': 2})

    def test_statistics_bivariate(self):
        self.run_two_party_test(microprotocol='StatisticsBivariate',
                                data_alice=[(1.0, 2.0)],
                                data_bob=[(2.0, 3.0)],
                                correct={'samples': 2,
                                         'covariance_mle': 0.25,
                                         'covariance': 0.5,
                                         'correlation_coefficient': 1.0,
                                         'regression_slope': 1.0,
                                         'regression_interceipt': 1.0,
                                         'regression_slope_only': 1.6})

    def test_statistics_frequency(self):
        self.run_two_party_test(microprotocol='StatisticsFrequency',
                                data_alice=['A', 'A', 'B', 'C', 'C', 'C'],
                                data_bob=['A', 'B', 'C', 'B', 'C', 'B', 'B', 'C', 'C'],
                                correct={'samples': 15,
                                         'mode': 'C',
                                         'histogram': {'A': 3, 'B': 5, 'C': 7}})

    def test_statistics_univariate(self):
        self.run_two_party_test(microprotocol='StatisticsUnivariate',
                                data_alice=[1.0, 2.0, 3.0, 4.0, 5.0],
                                data_bob=[6.0, 7.0, 8.0, 9.0, 10.0],
                                correct={'samples': 10,
                                         'minimum': 1.0,
                                         'maximum': 10.0,
                                         'sum': 55.0,
                                         'mean': 5.5,
                                         'harmonic_mean': 3.4141715214740550061,
                                         'geometric_mean': 4.5287286881167647622,
                                         'variance': 9.1666666666666666667,
                                         'variance_mle': 8.25,
                                         'variance_of_sample_mean': 0.91666666666666666667,
                                         'standard_deviation': 3.0276503540974916654,
                                         'standard_deviation_mle': 2.8722813232690143299,
                                         'standard_error_of_sample_mean': 0.95742710775633810998,
                                         'coefficient_of_variation': 0.55048188256318030280,
                                         'coefficient_of_variation_mle': 0.52223296786709351453,
                                         'root_mean_square': 6.2048368229954282981,
                                         'root_mean_square_deviation': 2.8722813232690143299,
                                         'skewness': 0.0,
                                         'kurtosis': 1.7757575757575757576,
                                         'kurtosis_excess': -1.2242424242424242424,
                                         'hyper_skewness': 0.0,
                                         'hyper_flatness': 3.7033976124885215794})

    def run_two_party_test(self, microprotocol, data_alice, data_bob, correct):

        interface_a = TestInterface()
        interface_b = TestInterface()
        interface_sync = TestInterface()

        network_a = {'nodes': [interface_a, interface_b], 'myself': 0}
        network_b = {'nodes': [interface_a, interface_b], 'myself': 1}

        api_a = TestApi(interface=interface_a)
        api_b = TestApi(interface=interface_b)
        api_sync = TestApi(interface=interface_sync)

        microservice_a = api_a.create(protocol="Simon")
        microservice_b = api_b.create(protocol="Simon")

        task_a = microservice_a.create_task(microprotocol=microprotocol, network=network_a)

        invitation_a = api_a.download(task_a.invite())

        api_sync.send_broadcast(invitation_a, ["invitation", "fdrtd-TestThreeParties"])

        invitation_b = api_sync.receive_broadcast(["invitation", "fdrtd-TestThreeParties"])
        task_b = microservice_b.join_task(invitation=invitation_b, network=network_b)

        task_a.input(data=data_alice)
        task_b.input(data=data_bob)

        task_a.start()
        task_b.start()

        repr_res_a = None
        while repr_res_a is None:
            repr_res_a = task_a.result()
        result_a = api_a.download(repr_res_a)
        self.assertEqual(result_a['inputs'], 2)
        for key in correct:
            self.outer_assertion(correct[key], result_a['result'][key], key)

    def run_three_party_test(self, microprotocol, data_alice, data_bob, data_charlie, correct):

        interface_a = TestInterface()
        interface_b = TestInterface()
        interface_c = TestInterface()
        interface_sync = TestInterface()

        network_a = {'nodes': [interface_a, interface_b, interface_c], 'myself': 0}
        network_b = {'nodes': [interface_a, interface_b, interface_c], 'myself': 1}
        network_c = {'nodes': [interface_a, interface_b, interface_c], 'myself': 2}

        api_a = TestApi(interface=interface_a)
        api_b = TestApi(interface=interface_b)
        api_c = TestApi(interface=interface_c)
        api_sync = TestApi(interface=interface_sync)

        microservice_a = api_a.create(protocol="Simon")
        microservice_b = api_b.create(protocol="Simon")
        microservice_c = api_c.create(protocol="Simon")

        task_a = microservice_a.create_task(microprotocol=microprotocol, network=network_a)

        invitation_a = api_a.download(task_a.invite())

        api_sync.send_broadcast(invitation_a, ["invitation", "fdrtd-TestThreeParties"])

        invitation_b = api_sync.receive_broadcast(["invitation", "fdrtd-TestThreeParties"])
        task_b = microservice_b.join_task(invitation=invitation_b, network=network_b)

        invitation_c = api_sync.receive_broadcast(["invitation", "fdrtd-TestThreeParties"])
        task_c = microservice_c.join_task(invitation=invitation_c, network=network_c)

        task_a.input(data=data_alice)
        task_b.input(data=data_bob)
        task_c.input(data=data_charlie)

        task_a.start()
        task_b.start()
        task_c.start()

        repr_res_a = None
        while repr_res_a is None:
            repr_res_a = task_a.result()
        result_a = api_a.download(repr_res_a)
        self.assertEqual(result_a['inputs'], 3)
        for key in correct:
            self.outer_assertion(correct[key], result_a['result'][key], key)
