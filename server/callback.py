from fdrtd.server.bus import get_bus


class Callback(dict):

    def __init__(self, handle, callback):

        # derive from dict so instances get auto serialized to JSON when passed as a parameter to an API call
        super().__init__(handle=handle, callback=callback)

    def __getattr__(self, attr):
        # instead of:
        # fdrtd.server.bus.get_bus().call_microservice(handle, "somefunction", parameters)
        # we may simply call:
        # handle.somefunction(parameters)
        if attr in self.__dict__:
            return super().__getattribute__(attr)
        if '__' in attr:  # do not make builtins available (potential vulnerabilities)
            raise AttributeError()
        return lambda **parameters: get_bus().call_microservice(handle=self['handle'],
                                                                function=attr,
                                                                parameters=parameters,
                                                                callback=self['callback'])
