import fdrtd.server.discovery
import fdrtd.server.exceptions
import uuid as _uuid


class Registry:

    def __init__(self):
        self.root_objects = {}
        fdrtd.server.discovery.discover_builtins_and_plugins(self)

    def register(self, identifiers, item):
        uuid = str(_uuid.uuid4())
        self.root_objects[uuid] = {'identifiers': identifiers, 'object': item}

    def list_representations(self):
        """list available server-side objects"""
        result = []
        for _, microservice in self.root_objects.items():
            result.append(microservice['identifiers'])
        return result

    def get_representation(self, requirements):

        def test(identifiers):
            for requirement in requirements:
                if requirement not in identifiers:
                    return False
                if identifiers[requirement] != requirements[requirement]:
                    return False
            return True

        for uuid, microservice in self.root_objects.items():
            if test(microservice['identifiers']):
                return uuid, microservice['object']

        raise fdrtd.server.exceptions.RootObjectNotFound(requirements)
