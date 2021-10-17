"""
contains microservice Barrier and its instances
"""

import uuid as _uuid

from fdrtd.server.microservice import Microservice


class Barrier(Microservice):
    """synchronizes parties through barriers"""

    def __init__(self, bus, endpoint):
        super().__init__(bus, endpoint)
        self.storage = {}

    def create(self, tokens):
        """creates a new barrier"""
        uuid = Barrier._create_deterministic_uuid(tokens)
        if uuid not in self.storage:
            self.storage[uuid] = BarrierInstance()
        return self.storage[uuid]

    def delete(self, uuid):
        """deletes a barrier"""
        del self.storage[uuid]

    @staticmethod
    def _create_deterministic_uuid(tokens):
        uuid = _uuid.UUID('fede1a7e-0010-4e73-865d-a8e55a223b63')
        uuid = _uuid.uuid5(uuid, 'Barrier')
        if tokens is not None:
            for token in tokens:
                uuid = _uuid.uuid5(uuid, token)
        return str(uuid)


class BarrierInstance:
    """a synchronization barrier"""

    def __init__(self):
        self.arrivals = set()
        self.departures = set()

    def arrive(self, party):
        """sets a parties state to arrived and resets departures"""
        self.arrivals.add(party)
        self.departures = set()

    def arrived(self):
        """returns the number of arrived parties"""
        return len(self.arrivals)

    def depart(self, party):
        """sets a parties state to departed"""
        self.departures.add(party)

    def departed(self):
        """returns the number of departed parties"""
        return len(self.departures)

    def reset(self):
        """resets arrivals"""
        self.arrivals = set()
