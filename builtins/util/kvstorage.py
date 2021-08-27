import uuid as _uuid

from fdrtd.server.microservice import Microservice


class KeyValueStorage(Microservice):

    def __init__(self, bus, endpoint):
        super().__init__(bus, endpoint)
        self.storages = {'default': {}}

    def create(self, value, storage='default'):
        if not storage in self.storages:
            self.storages[storage] = {}
        uuid = str(_uuid.uuid4())
        callback = {'uuid': uuid, 'storage': storage}
        self.store(value, callback)
        return self.callback(callback)

    def store(self, value, callback):
        kvstorage = self.storages[callback['storage']]
        kvstorage[callback['uuid']] = value
        return None

    def retrieve(self, callback):
        kvstorage = self.storages[callback['storage']]
        value = kvstorage[callback['uuid']]
        return value

    def exists(self, callback):
        kvstorage = self.storages[callback['storage']]
        return callback['uuid'] in kvstorage

    def delete(self, callback):
        kvstorage = self.storages[callback['storage']]
        del kvstorage[callback['uuid']]
        return None
