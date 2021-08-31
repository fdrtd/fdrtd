"""
contains microservice KeyValueStorage
"""

import uuid as _uuid

from fdrtd.server.microservice import Microservice


class KeyValueStorage(Microservice):
    """stores and retrieves values by key"""

    def __init__(self, bus, endpoint):
        super().__init__(bus, endpoint)
        self.storages = {'default': {}}

    def create(self, value, storage='default'):
        """create a storage; store value, return key"""
        if storage not in self.storages:
            self.storages[storage] = {}
        uuid = str(_uuid.uuid4())
        callback = {'uuid': uuid, 'storage': storage}
        self.store(value, callback)
        return self.callback(callback)

    def store(self, value, callback):
        """store value, return key"""
        kvstorage = self.storages[callback['storage']]
        kvstorage[callback['uuid']] = value

    def retrieve(self, callback):
        """retrieve value from storage"""
        kvstorage = self.storages[callback['storage']]
        value = kvstorage[callback['uuid']]
        return value

    def exists(self, callback):
        """return true if key exists in storage"""
        kvstorage = self.storages[callback['storage']]
        return callback['uuid'] in kvstorage

    def delete(self, callback):
        """delete key from storage"""
        kvstorage = self.storages[callback['storage']]
        del kvstorage[callback['uuid']]
