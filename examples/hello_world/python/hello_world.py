"""
hello world example

this example requires a single fdrtd server.

please see https://github.com/fdrtd/docs/wiki/how-to-run-a-fdrtd-server

then set the URL of the server accordingly below
"""


import representation


URL = "http://localhost:55501"


if __name__ == "__main__":
    api = representation.Api(URL)
    list_of_services = api.list()
    print(list_of_services)
