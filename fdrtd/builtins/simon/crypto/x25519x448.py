# the following code is in part derived from 'Code Components' published in:
# A. Langley, M. Hamburg, S. Turner: Elliptic Curves for Security
# Internet Research Task Force (IRTF) Request for Comments 7748 (January 2016)
# for the original document and code components see https://tools.ietf.org/html/rfc7748
# for licensing information see https://trustee.ietf.org/trust-legal-provisions.html:
# [quote] Code Components are also licensed to each person who wishes to receive such
# a license on the terms of the “Simplified BSD License", as described below [...]
#
# BSD License:
# Copyright (c) <insert year> IETF Trust and the persons identified as authors of the code. All rights reserved.
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
# * Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# * Neither the name of Internet Society, IETF or IETF Trust, nor the names of specific contributors,
#   may be used to endorse or promote products derived from this software without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS” AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


class X25519X448:

    def __init__(self, bits, p, a24, masked_key):
        self.bits = bits
        self.p = p
        self.a24 = a24
        self.mask = (1 << self.bits) - 1
        self.decoded_key = self.decode_little_endian(masked_key)

    def decode_little_endian(self, b):
        return sum([b[i] << 8 * i for i in range((self.bits + 7) // 8)])

    def decode_u_coordinate(self, u):
        u_list = [b for b in u]
        if self.bits % 8:
            u_list[-1] &= (1 << (self.bits % 8)) - 1
        return self.decode_little_endian(u_list)

    def encode_u_coordinate(self, u):
        u = u % self.p
        return bytes([((u >> 8 * i) & 0xff) for i in range((self.bits + 7) // 8)])

    def montgomery(self, k, u):
        x_1 = u
        x_2 = 1
        z_2 = 0
        x_3 = u
        z_3 = 1
        swap = 0
        for t in range(self.bits-1, -1, -1):
            k_t = (k >> t) & 1
            swap ^= k_t
            (x_2, x_3) = self.cswap(swap, x_2, x_3)
            (z_2, z_3) = self.cswap(swap, z_2, z_3)
            swap = k_t
            a = (x_2 + z_2) % self.p
            aa = pow(a, 2, self.p)
            b = (x_2 - z_2) % self.p
            bb = pow(b, 2, self.p)
            e = (aa - bb) % self.p
            c = (x_3 + z_3) % self.p
            d = (x_3 - z_3) % self.p
            da = (d * a) % self.p
            cb = (c * b) % self.p
            x_3 = pow(da + cb, 2, self.p)
            z_3 = (x_1 * pow(da - cb, 2, self.p)) % self.p
            x_2 = (aa * bb) % self.p
            z_2 = (e * (aa + self.a24 * e)) % self.p
        (x_2, x_3) = self.cswap(swap, x_2, x_3)
        (z_2, z_3) = self.cswap(swap, z_2, z_3)
        return (x_2 * pow(z_2, self.p - 2, self.p)) % self.p

    def cswap(self, swap, x_2, x_3):
        if swap:
            mask = self.mask
        else:
            mask = 0
        dummy = mask & (x_2 ^ x_3)
        x_2 = x_2 ^ dummy
        x_3 = x_3 ^ dummy
        return x_2, x_3

    def encrypt(self, data):
        k = self.decoded_key
        u = self.decode_u_coordinate(data)
        t = self.montgomery(k, u)
        return self.encode_u_coordinate(t)


class X25519(X25519X448):

    def __init__(self, secret_key):
        super().__init__(masked_key=self.mask_key(secret_key),
                         bits=255, p=2 ** 255 - 19, a24=121665)

    @staticmethod
    def mask_key(secret_key):
        masked_key = [b for b in secret_key]
        masked_key[0] &= 248
        masked_key[31] &= 127
        masked_key[31] |= 64
        return masked_key


class X448(X25519X448):

    def __init__(self, secret_key):
        super().__init__(masked_key=self.mask_key(secret_key),
                         bits=448, p=2 ** 448 - 2 ^ 224 - 1, a24=39081)

    @staticmethod
    def mask_key(secret_key):
        masked_key = [b for b in secret_key]
        masked_key[0] &= 252
        masked_key[55] |= 128
        return masked_key
