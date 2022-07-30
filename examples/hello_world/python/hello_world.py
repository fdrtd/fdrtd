"""
hello world example
"""


# we are using client-side representations of server-side objects
import representation


# the URL of your fdrtd server
URL = "http://localhost:55501"


if __name__ == "__main__":

    # connect to the fdrtd API
    api = representation.Api(URL)

    # fetch a list of available microservices
    list_of_services = api.list()

    print(list_of_services)
