import uuid as _uuid

from fdrtd.server.microservice import Microservice


class Barrier(Microservice):

    def __init__(self, bus, endpoint):
        super().__init__(bus, endpoint)
        self.storage = {}

    def create(self, tokens):
        uuid = Barrier._create_deterministic_uuid(tokens)
        if uuid not in self.storage:
            self.storage[uuid] = BarrierInstance()
        return self.callback(uuid)

    def arrive(self, callback, party):
        return self.storage[callback].arrive(party)

    def arrived(self, callback):
        return self.storage[callback].arrived()

    def depart(self, callback, party):
        return self.storage[callback].depart(party)

    def departed(self, callback):
        return self.storage[callback].departed()

    def reset(self, callback):
        return self.storage[callback].reset()

    def delete(self, callback):
        del self.storage[callback]
        return None

    @staticmethod
    def _create_deterministic_uuid(tokens):
        uuid = _uuid.UUID('fede1a7e-0010-4e73-865d-a8e55a223b63')
        uuid = _uuid.uuid5(uuid, 'Barrier')
        if tokens is not None:
            for token in tokens:
                uuid = _uuid.uuid5(uuid, token)
        return str(uuid)


class BarrierInstance:

    def __init__(self):
        self.arrivals = set()
        self.departures = set()

    def arrive(self, party):
        self.arrivals.add(party)
        self.departures = set()

    def arrived(self):
        return len(self.arrivals)

    def depart(self, party):
        self.departures.add(party)

    def departed(self):
        return len(self.departures)

    def reset(self):
        self.arrivals = set()
