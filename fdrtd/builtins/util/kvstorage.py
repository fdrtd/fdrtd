"""
contains microservice KeyValueStorage
"""


class KeyValueStorage:
    """stores and retrieves values by key"""

    def __init__(self):
        self.storages = {'default': {}}

    def create(self, storage='default'):
        """create a storage"""
        if storage not in self.storages:
            self.storages[storage] = KVStorage()
        return self.storages[storage]

    def delete(self, storage='default'):
        """delete a storage"""
        del self.storages[storage]
        return None


class KVStorage:

    def __init__(self):
        self.storage = {}

    def store(self, key, value):
        """store value, return key"""
        self.storage[key] = value

    def retrieve(self, key):
        """retrieve value from storage"""
        return self.storage.get(key, None)

    def exists(self, key):
        """return true if key exists in storage"""
        return key in self.storage

    def delete(self, key):
        """delete key from storage"""
        del self.storage[key]
