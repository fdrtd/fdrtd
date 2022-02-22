"""
contains class Microservice
"""

import fdrtd.server.exceptions


class Microservice:
    """base class for microservices"""

    def __init__(self, bus, handle):
        pass

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
