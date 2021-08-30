"""routines to interact with the bus of microservices"""

from flask import current_app

import fdrtd.server.exceptions


def get_bus():
    """get the singleton bus of the server application"""
    with current_app.app_context():
        return current_app.bus


class Bus:
    """the bus holds, selects, and calls microservices"""

    def __init__(self):
        """initialize the bus"""
        self.microservices = {}

    def set_microservices(self, microservices):
        """set microservices discovered on server startup (internal use only)"""
        self.microservices = microservices

    def list_microservices(self):
        """list all microservices and their public functions"""
        result = []
        for _, microservice in self.microservices.items():
            result.append({'identifiers': microservice['identifiers'],
                           'public': list(microservice['public'].keys())})
        return result

    def select_microservice(self, requirements):
        """select a microservice, given a number of key-value pairs"""

        def test(identifiers):
            for requirement in requirements:
                if requirement not in identifiers:
                    return False
                if identifiers[requirement] != requirements[requirement]:
                    return False
            return True

        for uuid, microservice in self.microservices.items():
            if test(microservice['identifiers']):
                return uuid

        raise fdrtd.server.exceptions.MicroserviceNotFound(requirements)

    def call_microservice(self, handle, function,
                          parameters=None, callback=None, public=False):
        """call a microservice by its handle, invoke one of its functions"""

        if handle not in self.microservices:
            raise fdrtd.server.exceptions.MicroserviceNotFound(handle)
        microservice = self.microservices[handle]

        if function in microservice['public']:
            pointer = microservice['public'][function]
        elif public:
            raise fdrtd.server.exceptions.FunctionNotPublic(function)
        elif function in microservice['private']:
            pointer = microservice['private'][function]
        else:
            raise fdrtd.server.exceptions.FunctionNotFound(function)

        if callback is None:
            result = pointer() if parameters is None else pointer(**parameters)
        else:
            result = pointer(callback=callback) if parameters is None\
                else pointer(**parameters, callback=callback)
        return result
