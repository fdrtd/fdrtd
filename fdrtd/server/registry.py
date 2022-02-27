"""the registry contains items that may be used as root items for representations"""

import uuid as _uuid

import fdrtd.server.discovery
import fdrtd.server.exceptions


class Registry:
    """records items and their descriptions for later use as representations"""

    def __init__(self):
        self.root_objects = {}
        fdrtd.server.discovery.discover_builtins_and_plugins(self)

    def register(self, description, item):
        """register an item and its description"""

        uuid = str(_uuid.uuid4())
        self.root_objects[uuid] = (description, item)

    def list_representations(self):
        """list available server-side objects"""

        result = []
        for _, (description, _) in self.root_objects.items():
            result.append(description)
        return result

    def get_representation(self, requirements):
        """check requirements against descriptions and return a matching item if possible"""

        for uuid, (description, item) in self.root_objects.items():
            for requirement in requirements:
                if requirement not in description:
                    break
                if description[requirement] != requirements[requirement]:
                    break
            else:
                return uuid, item

        raise fdrtd.server.exceptions.RootObjectNotFound(requirements)
