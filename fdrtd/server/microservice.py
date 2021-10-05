"""
contains class Microservice
"""

import fdrtd.server.exceptions
from fdrtd.server.callback import Callback


class Microservice:
    """base class for microservices"""

    def __init__(self, bus, handle):
        self.bus = bus
        self.handle = handle

    def callback(self, callback):
        """create a callback (used by child classes)"""
        return Callback(self.handle, callback)

    @staticmethod
    def make_public():
        """report public functions (will become obsolete!)
           note that child classes will overload this with make_public(self)"""
        return {}

    @staticmethod
    def safe_params(params, key):
        """helper routine, throws exception if key is not present in params"""
        if key not in params:
            raise fdrtd.server.exceptions.MissingParameter(key)
        return params[key]

    @staticmethod
    def safe_get(dictionary, key, keyname):
        """helper routine, throws exception if key is not present in dictionary"""
        if key not in dictionary:
            raise fdrtd.server.exceptions.InvalidIdentifier(keyname, key)
        return dictionary[key]

    @staticmethod
    def safe_delete(dictionary, key, keyname):
        """helper routine, throws exception if key is not present in dictionary"""
        if key not in dictionary:
            raise fdrtd.server.exceptions.InvalidIdentifier(keyname, key)
        del dictionary[key]
