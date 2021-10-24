from fdrtd.builtins.simon.caches.cache import Cache
from fdrtd.builtins.simon.microprotocols.microprotocol import Microprotocol
from fdrtd.builtins.common.accumulators.accumulator_statistics_bivariate import AccumulatorStatisticsBivariate


class MicroprotocolStatisticsBivariate(Microprotocol):

    def __init__(self, bus, properties, myself):
        super().__init__(bus, properties, myself)

        self.n = self.network.count

        self.digits_before = properties['parameters'].get('digits_before', 12)
        self.digits_after = properties['parameters'].get('digits_after', 12)

        self.register_cache('input', Cache())
        self.register_cache('x_uncentered_0', Cache())
        self.register_cache('x_uncentered_1', Cache())
        self.register_cache('x_uncentered_2', Cache())
        self.register_cache('x_uncentered_3', Cache())
        self.register_cache('x_uncentered_4', Cache())
        self.register_cache('x_uncentered_5', Cache())
        self.register_cache('x_samples', Cache())
        self.register_cache('x_geometric', Cache())
        self.register_cache('x_harmonic', Cache())
        self.register_cache('x_minmax', Cache())
        self.register_cache('y_uncentered_0', Cache())
        self.register_cache('y_uncentered_1', Cache())
        self.register_cache('y_uncentered_2', Cache())
        self.register_cache('y_uncentered_3', Cache())
        self.register_cache('y_uncentered_4', Cache())
        self.register_cache('y_uncentered_5', Cache())
        self.register_cache('y_samples', Cache())
        self.register_cache('y_geometric', Cache())
        self.register_cache('y_harmonic', Cache())
        self.register_cache('y_minmax', Cache())
        self.register_cache('xy_uncentered_0', Cache())
        self.register_cache('xy_uncentered_1', Cache())
        self.register_cache('xy_uncentered_2', Cache())
        self.register_cache('xy_uncentered_3', Cache())
        self.register_cache('xy_uncentered_4', Cache())
        self.register_cache('xy_uncentered_5', Cache())
        self.register_cache('xy_samples', Cache())
        self.register_cache('xy_geometric', Cache())
        self.register_cache('xy_harmonic', Cache())
        self.register_cache('xy_minmax', Cache())

        self.register_stage(0, ['input'], self.stage_0)
        self.register_stage(1, ['x_uncentered_0', 'x_uncentered_1', 'x_uncentered_2', 'x_uncentered_3', 'x_uncentered_4',
                                'x_uncentered_5', 'x_samples', 'x_geometric', 'x_harmonic', 'x_minmax'], self.stage_x)
        self.register_stage(2, ['y_uncentered_0', 'y_uncentered_1', 'y_uncentered_2', 'y_uncentered_3', 'y_uncentered_4',
                                'y_uncentered_5', 'y_samples', 'y_geometric', 'y_harmonic', 'y_minmax'], self.stage_y)
        self.register_stage(3, ['xy_uncentered_0', 'xy_uncentered_1', 'xy_uncentered_2', 'xy_uncentered_3', 'xy_uncentered_4',
                                'xy_uncentered_5', 'xy_samples', 'xy_geometric', 'xy_harmonic', 'xy_minmax'], self.stage_xy)

        self.input = None
        self.result_cache = AccumulatorStatisticsBivariate()

    def start_pipelines(self, prefix, accumulator):
        self.start_pipeline('BasicSum', prefix+'uncentered_0', accumulator.moments.uncentered[0])
        self.start_pipeline('BasicSum', prefix+'uncentered_1', accumulator.moments.uncentered[1])
        self.start_pipeline('BasicSum', prefix+'uncentered_2', accumulator.moments.uncentered[2])
        self.start_pipeline('BasicSum', prefix+'uncentered_3', accumulator.moments.uncentered[3])
        self.start_pipeline('BasicSum', prefix+'uncentered_4', accumulator.moments.uncentered[4])
        self.start_pipeline('BasicSum', prefix+'uncentered_5', accumulator.moments.uncentered[5])
        self.start_pipeline('BasicSum', prefix+'samples', accumulator.samples)
        self.start_pipeline('BasicSum', prefix+'geometric', accumulator.geometric)
        self.start_pipeline('BasicSum', prefix+'harmonic', accumulator.harmonic)
        self.start_pipeline('BasicMinMax', prefix+'minmax', [{'minimum': accumulator.minimum, 'maximum': accumulator.maximum}])

    def stage_0(self, args):
        self.input = AccumulatorStatisticsBivariate.deserialize(args['input'])
        self.start_pipelines('x_', self.input.accumulator_x)
        self.start_pipelines('y_', self.input.accumulator_y)
        self.start_pipelines('xy_', self.input.accumulator_xy)
        return 1, None

    def stage_z(self, args, prefix, accumulator):
        accumulator.moments.uncentered[0] = args[prefix+'uncentered_0']['sum']
        accumulator.moments.uncentered[1] = args[prefix+'uncentered_1']['sum']
        accumulator.moments.uncentered[2] = args[prefix+'uncentered_2']['sum']
        accumulator.moments.uncentered[3] = args[prefix+'uncentered_3']['sum']
        accumulator.moments.uncentered[4] = args[prefix+'uncentered_4']['sum']
        accumulator.moments.uncentered[5] = args[prefix+'uncentered_5']['sum']
        accumulator.samples = args[prefix+'samples']['sum']
        accumulator.geometric = args[prefix+'geometric']['sum']
        accumulator.harmonic = args[prefix+'harmonic']['sum']
        accumulator.minimum = args[prefix+'minmax']['minimum']
        accumulator.maximum = args[prefix+'minmax']['maximum']
        accumulator.moments.samples = accumulator.samples
        accumulator.moments.center = 0.0
        accumulator.moments.centered = [x for x in accumulator.moments.uncentered]
        accumulator.moments.set_center(accumulator.moments.uncentered[0] / accumulator.samples)

    def stage_x(self, args):
        self.stage_z(args, "x_", self.result_cache.accumulator_x)
        return 2, None

    def stage_y(self, args):
        self.stage_z(args, "y_", self.result_cache.accumulator_y)
        return 3, None

    def stage_xy(self, args):
        self.stage_z(args, "xy_", self.result_cache.accumulator_xy)
        return -1, {'inputs': self.n, 'result': self.result_cache.evaluate_to_dict()}
