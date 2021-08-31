"""
contains class Api
"""

from fdrtd.client.handle import Handle


class Api:
    """
    instances of API interact with the server-side fdrtd API
    """

    def __init__(self, interface):
        """initialise the API wrapper with an interface"""
        self.interface = interface

    def list_microservices(self):
        """retrieve a list of microservices from the server"""
        response, _ = self.interface.get()
        return response

    def select_microservice(self, **kwargs):
        """connect to a matching microservice"""
        response, _ = self.interface.put(body={**kwargs})
        endpoint = Handle(self, response, None)
        return endpoint

    def has_capabilities(self, **kwargs):
        """check if there is a matching microservice"""
        response, _ = self.interface.put(body={**kwargs})
        if response is None:
            return False
        return True

    def call_microservice(self, handle, function, parameters=None, callback=None):
        "call a microservice on the server"
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
