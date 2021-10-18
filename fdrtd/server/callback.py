"""
contains class Callback
"""


class Callback(dict):
    """Callback passes parameters from earlier API calls back to the server"""

    def __init__(self, handle, callback):

        # derive from dict so instances get auto serialized to JSON
        # when passed as a parameter to an API call
        super().__init__(handle=handle, callback=callback)
