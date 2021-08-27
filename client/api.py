from fdrtd.client.handle import Handle


class Api:

    def __init__(self, interface):
        self.interface = interface

    def list_microservices(self):
        response, code = self.interface.get()
        return response

    def select_microservice(self, **kwargs):
        response, code = self.interface.put(body={**kwargs})
        endpoint = Handle(self, response, None)
        return endpoint

    def has_capabilities(self, **kwargs):
        response, code = self.interface.put(body={**kwargs})
        if response is None:
            return False
        return True

    def call_microservice(self, handle, function, parameters=None, callback=None):
        response, code = self.interface.post(
            body={
                'handle': handle,
                'function': function,
                'parameters': parameters,
            } if callback is None else {
                'handle': handle,
                'function': function,
                'parameters': parameters,
                'callback': callback
            })
        if code == 200:
            return response
        if code == 201:
            return Handle(self, response['handle'], response['callback'])
        if code == 202:
            return Handle(self, response['handle'], None)
        if code == 204:
            return None
