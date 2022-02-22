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

    def create(self, uuid):
        """creates a new broadcast"""
        self.storage[uuid] = None
        return None

    def send(self, uuid, message):
        """stores a message to be broadcasted"""
        self.storage[uuid] = message

    def receive(self, uuid):
        """retrieves a broadcasted message"""
        return self.storage.get(uuid, None)

    def delete(self, uuid):
        """deletes a broadcast"""
        del self.storage[uuid]
