from fdrtd.server.bus import Bus
from fdrtd.server.discovery import discover_microservices


class TestInterface:

    def __init__(self):
        self.bus = Bus()
        microservices, classes = discover_microservices(self.bus)
        self.bus.set_microservices(microservices)
        self.bus.set_classes(classes)

    def post(self, *path, body=None):
        if len(path) == 1:
            if path[0] == 'representations':
                response = self.bus.create_representation(body)
                return {'type': 'uuid', 'uuid': response}, 200
        raise RuntimeError()

    def put(self, *path, body=None):
        if len(path) == 1:
            if path[0] == 'representations':
                response = self.bus.upload_representation(body)
                return {'type': 'uuid', 'uuid': response}, 200
        raise RuntimeError()

    def patch(self, *path, body=None):
        if len(path) == 2:
            if path[0] == 'representation':
                response = self.bus.call_representation(path[1], body)
                if response is None:
                    return {'type': 'none'}, 200
                return {'type': 'uuid', 'uuid': response}, 200
        raise RuntimeError()

    def get(self, *path):
        if len(path) == 1:
            if path[0] == 'representations':
                response = self.bus.list_representations()
                return {'type': 'list', 'list': response}, 200
        if len(path) == 2:
            if path[0] == 'representation':
                response = self.bus.download_representation(path[1])
                return {'type': 'object', 'object': response}, 200
        if len(path) == 3:
            if path[0] == 'representation':
                uuid = self.bus.create_attribute(path[1], path[2], public=True)
                return {'type': 'uuid', 'uuid': uuid}, 200
        raise RuntimeError()

    def delete(self, *path):
        if len(path) == 2:
            if path[0] == 'representation':
                self.bus.release_representation(path[1])
                return {'type': 'none'}, 200
        raise RuntimeError()
