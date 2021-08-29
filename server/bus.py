from flask import current_app

import fdrtd.server.exceptions


def get_bus():
    with current_app.app_context():
        return current_app.bus


class Bus:

    def __init__(self):
        self.microservices = {}

    def set_microservices(self, microservices):
        self.microservices = microservices

    def list_microservices(self):
        result = []
        for uuid, microservice in self.microservices.items():
            result.append({'identifiers': microservice['identifiers'],
                           'public': list(microservice['public'].keys())})
        return result

    def select_microservice(self, requirements):

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

    def call_microservice(self, handle, function, parameters=None, callback=None, public=False):

        if handle not in self.microservices:
            raise fdrtd.server.exceptions.MicroserviceNotFound(handle)
        microservice = self.microservices[handle]

        if function in microservice['public']:
            fn = microservice['public'][function]
        elif public:
            raise fdrtd.server.exceptions.FunctionNotPublic(function)
        elif function in microservice['private']:
            fn = microservice['private'][function]
        else:
            raise fdrtd.server.exceptions.FunctionNotFound(function)

        if callback is None:
            result = fn() if parameters is None else fn(**parameters)
        else:
            result = fn(callback=callback) if parameters is None else fn(**parameters, callback=callback)
        return result
