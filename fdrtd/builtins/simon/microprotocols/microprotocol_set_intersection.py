import binascii as _binascii
import secrets as _secrets
import hashlib as _hashlib

from fdrtd.builtins.simon.caches.cache import Cache
from fdrtd.builtins.simon.caches.additive import CacheAdditive
from fdrtd.builtins.simon.caches.functional import CacheFunctional
from fdrtd.builtins.simon.microprotocols.microprotocol import Microprotocol
from fdrtd.builtins.simon.crypto.x25519x448 import X25519


class MicroprotocolSetIntersection(Microprotocol):

    def __init__(self, bus, properties, myself):
        super().__init__(bus, properties, myself)

        self.secret_key = _secrets.token_bytes(32)

        self.n = len(properties['nodes'])

        self.register_cache('input', Cache())
        self.register_stage(0, ['input'], self.stage_0)

        for i in range(self.n-1):
            self.register_cache('stage{}'.format(i+1), Cache())
            self.register_stage(i+1, ['stage{}'.format(i+1)], self.stage_i)

        self.register_cache('stage{}'.format(self.n), CacheFunctional(lambda x, y: set(x).intersection(set(y)), self.n, self.n))
        self.register_stage(self.n, ['stage{}'.format(self.n)], self.stage_n)

        self.register_cache('reverse', Cache())
        self.register_stage(self.n+1, ['reverse'], self.stage_reverse)

        self.register_cache('samples', CacheAdditive(minimum=self.n))

        self.register_cache('final', Cache())
        self.register_stage(self.n+2, ['final', 'samples'], self.stage_final)

        self.sizes = [0] * self.n
        self.lut = {}
        self.input_lut = {}

    def stage_0(self, args):
        self.network.broadcast(args['input']['samples'], 'samples')
        encrypted = []
        for item in args['input']['set']:
            enc = _hashlib.sha3_256(item.encode("utf-8")).hexdigest()
            self.input_lut[enc] = item
            encrypted.append(enc)
        return self.stage_i({'stage': 0, 'stage0': encrypted})

    def stage_i(self, args):
        stage = args['stage']
        xh = args['stage{}'.format(stage)]
        self.sizes[(self.network.myself-stage) % self.n] = len(xh)
        xxh = self.encrypt(xh)
        if stage == self.network.myself:
            for i in range(len(xxh)):
                self.lut[xxh[i]] = xh[i]
        if stage+1 < self.n:
            self.network.send_to_next_node(xxh, 'stage{}'.format(stage+1))
        else:
            self.network.broadcast(xxh, 'stage{}'.format(stage+1))
        return stage+1, None

    def stage_n(self, args):
        stage = args['stage']
        xxh = args['stage{}'.format(stage)]
        if self.network.myself == self.n-1:
            self.stage_reverse({'stage': stage, 'reverse': xxh})
            return stage + 2, None
        return stage + 1, None

    def stage_reverse(self, args):
        xh = [self.lut[encrypted] for encrypted in args['reverse']]
        if self.network.myself == 0:
            self.network.broadcast(xh, 'final')
        else:
            self.network.send_to_previous_node(xh, 'reverse')
        return args['stage'] + 1, None

    def stage_final(self, args):
        return -1, {'inputs': self.n,
                    'result': {
                        'samples': args['samples'],
                        'size_data': self.sizes,
                        'size_intersection': len(args['final']),
                        'intersection': [self.input_lut[enc] for enc in args['final']]}}

    def encrypt(self, data):
        x25519 = X25519(self.secret_key)
        return [_binascii.hexlify(x25519.encrypt(_binascii.unhexlify(d))).decode('utf-8') for d in data]
