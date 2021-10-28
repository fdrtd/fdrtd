from fdrtd.builtins.simon.caches.cache import Cache
from fdrtd.builtins.simon.microprotocols.microprotocol import Microprotocol
from fdrtd.builtins.simon.accumulators.accumulator_statistics_univariate import AccumulatorStatisticsUnivariate


class MicroprotocolStatisticsUnivariate(Microprotocol):

    def __init__(self, bus, properties, myself):
        super().__init__(bus, properties, myself)

        self.n = self.network.count

        self.digits_before = properties['parameters'].get('digits_before', 12)
        self.digits_after = properties['parameters'].get('digits_after', 12)

        self.register_cache('input', Cache())
        self.register_cache('uncentered_0', Cache())
        self.register_cache('uncentered_1', Cache())
        self.register_cache('uncentered_2', Cache())
        self.register_cache('uncentered_3', Cache())
        self.register_cache('uncentered_4', Cache())
        self.register_cache('uncentered_5', Cache())
        self.register_cache('samples', Cache())
        self.register_cache('geometric', Cache())
        self.register_cache('harmonic', Cache())
        self.register_cache('minmax', Cache())

        self.register_stage(0, ['input'], self.stage_0)
        self.register_stage(1, ['uncentered_0', 'uncentered_1', 'uncentered_2', 'uncentered_3', 'uncentered_4',
                                'uncentered_5', 'samples', 'geometric', 'harmonic', 'minmax'], self.stage_1)

        self.input = None
        self.result_cache = AccumulatorStatisticsUnivariate()

    def stage_0(self, args):
        self.input = AccumulatorStatisticsUnivariate.deserialize(args['input'])
        self.start_pipeline('BasicSum', 'uncentered_0', self.input.moments.uncentered[0])
        self.start_pipeline('BasicSum', 'uncentered_1', self.input.moments.uncentered[1])
        self.start_pipeline('BasicSum', 'uncentered_2', self.input.moments.uncentered[2])
        self.start_pipeline('BasicSum', 'uncentered_3', self.input.moments.uncentered[3])
        self.start_pipeline('BasicSum', 'uncentered_4', self.input.moments.uncentered[4])
        self.start_pipeline('BasicSum', 'uncentered_5', self.input.moments.uncentered[5])
        self.start_pipeline('BasicSum', 'samples', self.input.samples)
        self.start_pipeline('BasicSum', 'geometric', self.input.geometric)
        self.start_pipeline('BasicSum', 'harmonic', self.input.harmonic)
        self.start_pipeline('BasicMinMax', 'minmax', [{'minimum': self.input.minimum, 'maximum': self.input.maximum}])
        return 1, None

    def stage_1(self, args):
        self.result_cache.moments.uncentered[0] = args['uncentered_0']['sum']
        self.result_cache.moments.uncentered[1] = args['uncentered_1']['sum']
        self.result_cache.moments.uncentered[2] = args['uncentered_2']['sum']
        self.result_cache.moments.uncentered[3] = args['uncentered_3']['sum']
        self.result_cache.moments.uncentered[4] = args['uncentered_4']['sum']
        self.result_cache.moments.uncentered[5] = args['uncentered_5']['sum']
        self.result_cache.samples = args['samples']['sum']
        self.result_cache.geometric = args['geometric']['sum']
        self.result_cache.harmonic = args['harmonic']['sum']
        self.result_cache.minimum = args['minmax']['minimum']
        self.result_cache.maximum = args['minmax']['maximum']
        self.result_cache.moments.samples = self.result_cache.samples
        self.result_cache.moments.center = 0.0
        self.result_cache.moments.centered = [x for x in self.result_cache.moments.uncentered]
        self.result_cache.moments.set_center(self.result_cache.moments.uncentered[0] / self.result_cache.samples)
        return -1, {'inputs': self.n, 'result': self.result_cache.evaluate_to_dict()}
