class Handle(dict):

    def __init__(self, api, handle, callback):

        # derive from dict so instances get auto serialized to JSON when passed as a parameter to an API call
        super().__init__(handle=handle, callback=callback)

        # however, api is a client-side instance and should not get serialized, so lives outside of the dict
        self.api = api

    def __getattr__(self, attr):
        # instead of:
        # api.call_microservice(handle, "somefunction", parameters)
        # we may simply call:
        # handle.somefunction(parameters)
        if attr in self.__dict__:
            return super().__getattr__(attr)
        return lambda **parameters: self.api.call_microservice(handle=self['handle'],
                                                               function=attr,
                                                               parameters=parameters,
                                                               callback=self['callback'])
