import secrets as _secrets

from fdrtd.builtins.simon.caches.cache import Cache
from fdrtd.builtins.simon.caches.additive import CacheAdditive
from fdrtd.builtins.simon.microprotocols.microprotocol import Microprotocol


class MicroprotocolBasicSum(Microprotocol):

    def __init__(self, bus, properties, myself):
        super().__init__(bus, properties, myself)

        self.n = self.network.count

        self.digits_before = properties['parameters'].get('digits_before', 12)
        self.digits_after = properties['parameters'].get('digits_after', 12)

        self.intermediate = 0

        self.register_cache('input', Cache())
        self.register_cache('samples', CacheAdditive(minimum=self.n))
        self.register_cache('intermediate', CacheAdditive(minimum=self.n))
        self.register_cache('final', CacheAdditive(minimum=self.n))

        self.register_stage(0, ['input'], self.stage_0)
        self.register_stage(1, ['intermediate'], self.stage_1)
        self.register_stage(2, ['final'], self.stage_2)

    def stage_0(self, args):
        self.network.broadcast(args['input']['samples'], 'samples')
        o = args['input']['sum']
        s = 0
        for i in range(self.network.count - 1):
            r = _secrets.randbelow(10 ** (self.digits_after+self.digits_before))
            s = s + r
            self.network.send_to_node(r, i, 'intermediate')
        self.network.send_to_node(int(o * (10 ** self.digits_after)) - s, self.network.count - 1, 'intermediate')
        return 1, None

    def stage_1(self, args):
        self.network.broadcast(args['intermediate'], 'final')
        return 2, None

    def stage_2(self, args):
        return -1, {'inputs': self.n,
                    'result': {
                        'samples': self.caches['samples'].get_data(),
                        'sum': args['final'] / (10 ** self.digits_after)}}
