from representation import Api


class SyncApi(Api):

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
        if rec is None:
            return None
        return self.download(rec)

    def clear_broadcast(self, tokens=None):
        ms = self.create(plugin="Sync", microservice='Broadcast')
        sync = ms.create(tokens=tokens)
        return sync.delete()

    def wait_for_broadcast(self, tokens=None):
        ms = self.create(plugin="Sync", microservice='Broadcast')
        sync = ms.create(tokens=tokens)
        rec = None
        while rec is None:
            rec = sync.receive()
        return self.download(rec)
