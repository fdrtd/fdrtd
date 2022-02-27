from fdrtd.server.discovery import discover_builtins_and_plugins
import fdrtd.server.exceptions

class Registry:

    def __init__(self):
        self.root_objects = discover_builtins_and_plugins()

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
