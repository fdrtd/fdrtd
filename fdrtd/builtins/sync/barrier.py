"""
contains microservice Barrier and its instances
"""


class Barrier:
    """synchronizes parties through barriers"""

    def __init__(self):
        self.storage = {}

    def create(self, uuid):
        """creates a new barrier"""
        if uuid not in self.storage:
            self.storage[uuid] = BarrierInstance()
        return self.storage[uuid]

    def delete(self, uuid):
        """deletes a barrier"""
        del self.storage[uuid]


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
