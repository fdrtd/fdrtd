"""
hello world example

a single fdrtd server is needed for this example.
the easiest way is to run one on localhost:

    pip install fdrtd
    python -m fdrtd.webserver --port=55500

then, the following script may be executed.
"""


import fdrtd.client


URL = "http://localhost:55500"


if __name__ == "__main__":
    api = fdrtd.client.Api(URL)
    list_of_services = api.list()
    print(list_of_services)
