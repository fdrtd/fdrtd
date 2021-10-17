"""routines to interact with the bus of microservices"""

import uuid as _uuid

from flask import current_app

import fdrtd.server.exceptions


def get_bus():
    """get the singleton bus of the server application"""
    with current_app.app_context():
        return current_app.bus


class MicroserviceWrapper:
    def __init__(self, microservice):
        self.microservice = microservice


class Bus:
    """the bus stores representations of microservices and other server-side objects"""

    def __init__(self):
        """initialize the bus"""
        self.microservices = {}
        self.lut_uuid_to_repr = {}

    def set_microservices(self, microservices):
        """set microservices discovered on server startup (internal use only)"""
        self.microservices = microservices

    def get_argument(self, arg):
        if isinstance(arg, dict):
            if 'representation_uuid' in arg:
                if arg['representation_uuid'] in self.lut_uuid_to_repr:
                    return self.get_argument(self.lut_uuid_to_repr[arg['representation_uuid']])
                else:
                    return arg
            else:
                return arg
        else:
            return arg

    def get_arguments(self, body):
        args = body['args']
        kwargs = {}
        for k in body['kwargs']:
            kwargs[k] = self.get_argument(body['kwargs'][k])
        return args, kwargs

    def list_representations(self):
        """list available server-side objects"""
        result = []
        for _, microservice in self.microservices.items():
            result.append({'identifiers': microservice['identifiers'],
                           'public': list(microservice['public'].keys())})
        return result

    def create_representation(self, body):
        """create a representation"""
        args = body['args']
        kwargs = body['kwargs']

        requirements = kwargs
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
                if uuid not in self.lut_uuid_to_repr:
                    wrapper = MicroserviceWrapper(microservice)
                    self.lut_uuid_to_repr[uuid] = wrapper
                return uuid

        raise fdrtd.server.exceptions.MicroserviceNotFound(requirements)

    def upload_representation(self, body):
        """upload an object, and return its representation"""
        args, kwargs = self.get_arguments(body)
        uuid = str(_uuid.uuid4())
        self.lut_uuid_to_repr[uuid] = args[0]
        return uuid

    def call_representation(self, representation_uuid, body):
        """call a server-side object"""
        args, kwargs = self.get_arguments(body)
        pointer = self.lut_uuid_to_repr[representation_uuid]
        if isinstance(pointer, dict):
            fn = self.lut_uuid_to_repr[pointer['pointer']]
            result = fn(*args, **kwargs, callback=pointer['callback'])
        else:
            result = pointer(*args, **kwargs)
        uuid = str(_uuid.uuid4())
        self.lut_uuid_to_repr[uuid] = result
        return uuid

    def download_representation(self, representation_uuid):
        """download a serialized version of a server-side object"""
        return self.lut_uuid_to_repr[representation_uuid]

    def release_representation(self, representation_uuid):
        """release a representation"""
        del self.lut_uuid_to_repr[representation_uuid]

    def create_attribute(self, representation_uuid, attribute_name, public=False):
        """create a representation of an attribute of a representation"""

        import fdrtd.server.callback

        if representation_uuid in self.microservices:
            instance = self.microservices[representation_uuid]
        else:
            wrapper = self.lut_uuid_to_repr[representation_uuid]
            if isinstance(wrapper, MicroserviceWrapper):
                instance = wrapper.microservice
            else:
                instance = wrapper

        if isinstance(instance, fdrtd.server.callback.Callback):
            pointer = getattr(instance, attribute_name)
        elif isinstance(instance, dict):
            if attribute_name in instance['public']:
                pointer = instance['public'][attribute_name]
            elif public:
                raise fdrtd.server.exceptions.FunctionNotPublic(attribute_name)
            elif attribute_name in instance['private']:
                pointer = instance['private'][attribute_name]
            else:
                raise fdrtd.server.exceptions.FunctionNotFound(attribute_name)
        else:
            try:
                pointer = getattr(instance, attribute_name)
            except KeyError:
                raise fdrtd.server.exceptions.FunctionNotFound(attribute_name)

        uuid = str(_uuid.uuid4())
        self.lut_uuid_to_repr[uuid] = pointer
        return uuid
