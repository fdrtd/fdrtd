"""routines to interact with the bus of microservices"""

import uuid as _uuid

import fdrtd.server.exceptions
from fdrtd.server.registry import Registry


class Bus:
    """the bus stores representations of microservices and other server-side objects"""

    def __init__(self):
        """initialize the bus"""
        self.lut_uuid_to_repr = {}
        self.registry = Registry()

    def get_argument(self, arg):
        if isinstance(arg, dict):
            if 'representation_uuid' in arg:
                if arg['representation_uuid'] in self.lut_uuid_to_repr:
                    return self.get_argument(self.lut_uuid_to_repr[arg['representation_uuid']])
        return arg

    def get_arguments(self, body):
        args = body.get('args', [])
        kwargs = {}
        for k in body.get('kwargs', {}):
            kwargs[k] = self.get_argument(body['kwargs'][k])
        return args, kwargs

    def list_representations(self):
        """list available server-side objects"""
        return self.registry.list_representations()

    def create_representation(self, body):
        """create a representation"""
        _, requirements = self.get_arguments(body)
        uuid, representation = self.registry.get_representation(requirements)

        if uuid not in self.lut_uuid_to_repr:
            self.lut_uuid_to_repr[uuid] = representation

        return uuid

    def upload_representation(self, body):
        """upload an object, and return its representation"""
        args, _ = self.get_arguments(body)
        uuid = str(_uuid.uuid4())
        self.lut_uuid_to_repr[uuid] = args[0]
        return uuid

    def call_representation(self, representation_uuid, body):
        """call a server-side object"""
        args, kwargs = self.get_arguments(body)
        pointer = self.lut_uuid_to_repr[representation_uuid]
        if isinstance(pointer, dict):
            function = self.lut_uuid_to_repr[pointer['pointer']]
            result = function(*args, **kwargs, callback=pointer['callback'])
        else:
            result = pointer(*args, **kwargs)
        if result is None:
            return None
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

        if public and attribute_name[0] == '_':  # public access to private/hidden member
            raise fdrtd.server.exceptions.AttributeNotPublic(attribute_name)

        try:
            obj = self.lut_uuid_to_repr[representation_uuid]
        except KeyError as key_error:
            raise fdrtd.server.exceptions.InvalidIdentifier("representation_uuid",
                                                            representation_uuid) from key_error

        try:
            pointer = getattr(obj, attribute_name)
        except KeyError as key_error:
            raise fdrtd.server.exceptions.AttributeNotFound(attribute_name) from key_error

        uuid = str(_uuid.uuid4())
        self.lut_uuid_to_repr[uuid] = pointer
        return uuid
