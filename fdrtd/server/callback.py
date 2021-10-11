"""
contains class Callback
"""

from fdrtd.server.bus import get_bus


class Callback(dict):
    """Callback passes parameters from earlier API calls back to the server"""

    def __init__(self, handle, callback):

        # derive from dict so instances get auto serialized to JSON
        # when passed as a parameter to an API call
        super().__init__(handle=handle, callback=callback)

    def __getattr__(self, attr):

        # instead of:
        # fdrtd.server.bus.get_bus().call_microservice(handle, "somefunction", parameters)
        # we may simply call:
        # handle.somefunction(parameters)
        if attr in self.__dict__:
            return super().__getattribute__(attr)

        # do not make builtins available (potential vulnerabilities)
        if '__' in attr:
            raise AttributeError()

        return {'pointer': get_bus().create_attribute(representation_uuid=self['handle'], attribute_name=attr),
                'callback': self['callback']}
