"""
contains class Handle
"""


class Handle(dict):

    """
    instances of Handle contain references to server-side objects
    """

    def __init__(self, api, handle, callback):

        # derive from dict so instances get auto serialized
        # to JSON when passed as a parameter to an API call
        super().__init__(handle=handle, callback=callback)

        # however, api is a client-side instance and should
        # not get serialized, so lives outside of the dict
        self.api = api

    def __getattr__(self, attr):

        """
        calling a virtual member function of the handle invokes the respective
        member function of the server-side microservice with callback parameters.

        instead of:
        api.call_microservice(handle, "somefunction", parameters)
        we may simply call:
        handle.somefunction(parameters)
        """

        if attr in self.__dict__:
            return super().__getattr__(attr)
        return lambda **parameters: self.api.call_microservice(handle=self['handle'],
                                                               function=attr,
                                                               parameters=parameters,
                                                               callback=self['callback'])
