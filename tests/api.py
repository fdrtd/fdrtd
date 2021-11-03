from fdrtd.clients.python import Api


class TestApi(Api):

    def join_barrier(self, parties, party, tokens=None):
        ms = self.create(plugin="Sync", microservice='Barrier')
        sync = ms.create(tokens=tokens)
        sync.arrive(party=party)
        while sync.arrived() < parties:
            pass
        sync.depart(party=party)
        while sync.departed() < parties:
            pass
        return sync.reset()

    def send_broadcast(self, message, tokens=None):
        ms = self.create(plugin="Sync", microservice='Broadcast')
        sync = ms.create(tokens=tokens)
        return sync.send(message=message)

    def receive_broadcast(self, tokens=None):
        ms = self.create(plugin="Sync", microservice='Broadcast')
        sync = ms.create(tokens=tokens)
        rec = sync.receive()
        return self.download(rec)

    def clear_broadcast(self, tokens=None):
        ms = self.create(plugin="Sync", microservice='Broadcast')
        sync = ms.create(tokens=tokens)
        return sync.delete()

    def wait_for_broadcast(self, tokens=None):
        response = None
        while not response:
            response = self.receive_broadcast(tokens)
        return response
