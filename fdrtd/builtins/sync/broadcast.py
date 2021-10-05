"""
contains microservice Broadcast
"""

import uuid as _uuid

from fdrtd.server.microservice import Microservice


class Broadcast(Microservice):
    """synchronizes parties through broadcasts"""

    def __init__(self, bus, endpoint):
        super().__init__(bus, endpoint)
        self.storage = {}

    def create(self, tokens):
        """creates a new broadcast"""
        uuid = Broadcast._create_deterministic_uuid(tokens)
        return self.callback(uuid)

    def send(self, callback, message):
        """stores a message to be broadcasted"""
        self.storage[callback] = message

    def receive(self, callback):
        """retrieves a broadcasted message"""
        return self.storage.get(callback, None)

    def delete(self, callback):
        """deletes a broadcast"""
        del self.storage[callback]

    @staticmethod
    def _create_deterministic_uuid(tokens):
        uuid = _uuid.UUID('fede1a7e-0010-4e73-865d-a8e55a223b63')
        uuid = _uuid.uuid5(uuid, 'Broadcast')
        if tokens is not None:
            for token in tokens:
                uuid = _uuid.uuid5(uuid, token)
        return str(uuid)
