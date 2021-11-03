"""
contains class Representation
"""


class Representation(dict):

    """
    a representation is a client-side reference to a server-side object
    """

    def __init__(self, api, representation_uuid):

        # derive from dict so instances get auto serialized
        # to JSON when passed as a parameter to an API call
        super().__init__(representation_uuid=representation_uuid)

        # however, api is a client-side instance and should
        # not get serialized, so lives outside of the dict
        self.api = api

    def __getattr__(self, member_name):
        if member_name in self.__dict__:
            return super().__getattr__(member_name)
        return self.api.attribute(self['representation_uuid'], member_name)

    def __call__(self, *args, **kwargs):
        return self.api.call(self['representation_uuid'], *args, **kwargs)
