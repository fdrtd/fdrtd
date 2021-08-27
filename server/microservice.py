import fdrtd.server.exceptions
from fdrtd.server.callback import Callback


class Microservice(object):

    def __init__(self, bus, handle):
        self.bus = bus
        self.handle = handle

    def callback(self, callback):
        return Callback(self.handle, callback)

    def make_public(self):
        return {}

    @staticmethod
    def safe_params(params, key):
        if key not in params:
            raise fdrtd.server.exceptions.MissingParameter(key)
        return params[key]

    @staticmethod
    def safe_get(dictionary, key, keyname):
        if key not in dictionary:
            raise fdrtd.server.exceptions.InvalidIdentifier(keyname, key)
        return dictionary[key]

    @staticmethod
    def safe_delete(dictionary, key, keyname):
        if key not in dictionary:
            raise fdrtd.server.exceptions.InvalidIdentifier(keyname, key)
        del dictionary[key]
        return None
