import fdrtd.server.discovery
import fdrtd.server.exceptions
import uuid as _uuid


class Registry:

    def __init__(self):
        self.root_objects = {}
        fdrtd.server.discovery.discover_builtins_and_plugins(self)

    def register(self, description, item):
        uuid = str(_uuid.uuid4())
        self.root_objects[uuid] = (description, item)

    def list_representations(self):
        """list available server-side objects"""
        result = []
        for _, (description, item) in self.root_objects.items():
            result.append(description)
        return result

    def get_representation(self, requirements):

        for uuid, (description, item) in self.root_objects.items():
            for requirement in requirements:
                if requirement not in description:
                    break
                if description[requirement] != requirements[requirement]:
                    break
            else:
                return uuid, item

        raise fdrtd.server.exceptions.RootObjectNotFound(requirements)
