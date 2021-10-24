from fdrtd.builtins.simon.caches.cache import Cache
from fdrtd.builtins.simon.caches.functional import CacheFunctional
from fdrtd.builtins.simon.caches.additive import CacheAdditive
from fdrtd.builtins.simon.microprotocols.microprotocol import Microprotocol


class MicroprotocolBasicMinMax(Microprotocol):

    def __init__(self, bus, properties, myself):
        super().__init__(bus, properties, myself)

        self.n = self.network.count

        self.intermediate = 0

        self.register_cache('input', Cache())
        self.register_cache('samples', CacheAdditive(minimum=self.n))
        self.register_cache('minimum', CacheFunctional(lambda x, y: x if x < y else y, minimum=self.n))
        self.register_cache('maximum', CacheFunctional(lambda x, y: x if x > y else y, minimum=self.n))

        self.register_stage(0, ['input'], self.stage_0)
        self.register_stage(1, ['samples', 'minimum', 'maximum'], self.stage_1)

    def stage_0(self, args):
        self.network.broadcast(args['input']['samples'], 'samples')
        self.network.broadcast(args['input']['minimum'], 'minimum')
        self.network.broadcast(args['input']['maximum'], 'maximum')
        return 1, None

    def stage_1(self, args):
        return -1, {'inputs': self.n,
                    'result': {
                        'samples': args['samples'],
                        'minimum': args['minimum'],
                        'maximum': args['maximum']}}
