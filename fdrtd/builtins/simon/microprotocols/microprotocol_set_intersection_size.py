import binascii as _binascii
import secrets as _secrets
import hashlib as _hashlib

from fdrtd.builtins.simon.caches.cache import Cache
from fdrtd.builtins.simon.caches.additive import CacheAdditive
from fdrtd.builtins.simon.caches.functional import CacheFunctional
from fdrtd.builtins.simon.microprotocols.microprotocol import Microprotocol
from fdrtd.builtins.simon.crypto.x25519x448 import X25519


class MicroprotocolSetIntersectionSize(Microprotocol):

    def __init__(self, bus, properties, myself):
        super().__init__(bus, properties, myself)

        self.secret_key = _secrets.token_bytes(32)

        self.n = len(properties['nodes'])

        self.register_cache('input', Cache())
        self.register_stage(0, ['input'], self.stage_0)

        for i in range(self.n-1):
            self.register_cache('stage{}'.format(i+1), Cache())
            self.register_stage(i+1, ['stage{}'.format(i+1)], self.stage_i)

        self.register_cache('stage{}'.format(self.n), CacheFunctional(lambda x, y: set(x).intersection(set(y)), self.n, self.n))  # lambda x, y: set(x).intersection(set(y)), n, n))
        self.register_stage(self.n, ['stage{}'.format(self.n), 'samples'], self.stage_n)

        self.register_cache('samples', CacheAdditive(minimum=self.n))

        self.sizes = [0] * self.n

    def stage_0(self, args):
        self.network.broadcast(args['input']['samples'], 'samples')
        return self.stage_i({'stage': 0, 'stage0': [_hashlib.sha3_256(item.encode("utf-8")).hexdigest() for item in args['input']['set']]})

    def stage_i(self, args):
        stage = args['stage']
        xh = args['stage{}'.format(stage)]
        self.sizes[(self.network.myself-stage) % self.n] = len(xh)
        xxh = self.encrypt(xh)
        if stage+1 < self.n:
            self.network.send_to_next_node(xxh, 'stage{}'.format(stage+1))
        else:
            self.network.broadcast(xxh, 'stage{}'.format(stage+1))
        return stage+1, None

    def stage_n(self, args):
        return -1, {'inputs': self.n,
                    'result': {
                        'samples': args['samples'],
                        'size_data': self.sizes,
                        'size_intersection': len(args['stage{}'.format(args['stage'])])}}

    def encrypt(self, data):
        x25519 = X25519(self.secret_key)
        return [_binascii.hexlify(x25519.encrypt(_binascii.unhexlify(d))).decode('utf-8') for d in data]
