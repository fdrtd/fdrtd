"""
contains class Api
"""

from fdrtd.clients.python.interfaces.http import HttpInterface
from fdrtd.clients.python.representation import Representation


class Api:

    """
    Api is a wrapper for the representation API endpoints
    """

    def __init__(self, url=None, interface=None):
        if url is not None:
            self.interface = HttpInterface(url)
        elif interface is not None:
            self.interface = interface

    def list(self):
        response, _ = self.interface.get('representations')
        return response['list']

    def create(self, *args, **kwargs):
        response, _ = self.interface.post('representations', body={'args': args, 'kwargs': kwargs})
        endpoint = Representation(self, response['uuid'])
        return endpoint

    def upload(self, *args, **kwargs):
        response, _ = self.interface.put('representations', body={'args': args, 'kwargs': kwargs})
        endpoint = Representation(self, response['uuid'])
        return endpoint

    def call(self, representation_uuid, *args, **kwargs):
        response, _ = self.interface.patch('representation', representation_uuid, body={'args': args, 'kwargs': kwargs})
        if response['type'] == 'uuid':
            endpoint = Representation(self, response['uuid'])
            return endpoint
        return None

    def download(self, representation):
        response, _ = self.interface.get('representation', representation['representation_uuid'])
        return response['object']

    def release(self, representation_uuid):
        self.interface.delete('representation', representation_uuid)
        return None

    def attribute(self, representation_uuid, member_name):
        response, _ = self.interface.get('representation', representation_uuid, member_name)
        endpoint = Representation(self, response['uuid'])
        return endpoint
