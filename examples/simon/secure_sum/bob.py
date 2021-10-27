"""
secure sum example with Simon

four fdrtd servers are needed for this example.
one for each of Alice, Bob, and Charlie.
and an additional one for invitations and synchronizing.
the easiest way is to run them all on localhost:

    pip install fdrtd
    python -m fdrtd.webserver --port=55500 &
    python -m fdrtd.webserver --port=55501 &
    python -m fdrtd.webserver --port=55502 &
    python -m fdrtd.webserver --port=55503 &

then, the three scripts of Alice, Bob, and Charlie may be executed simultaneously.
"""


import representation
from tools.sync import SyncApi


URL_SYNC = "http://127.0.0.1:55500"
URL_ALICE = "http://127.0.0.1:55501"
URL_BOB = "http://127.0.0.1:55502"
URL_CHARLIE = "http://127.0.0.1:55503"

SECRET_BOB = 16.0
NETWORK_BOB = {'nodes': [URL_ALICE, URL_BOB, URL_CHARLIE], 'myself': 1}  # Bob is no. 1 out of 0, 1, 2.
SHARED_TOKENS = ["Some", "Shared", "Tokens"]  # Shared by Alice, Bob, and Charlie; for synchronization


if __name__ == "__main__":

    api = representation.Api(URL_BOB)
    api_sync = SyncApi(URL_SYNC)

    microservice = api.create(protocol="Simon")
    invitation = api_sync.wait_for_broadcast(tokens=SHARED_TOKENS)
    task = microservice.join_task(invitation=invitation, network=NETWORK_BOB)
    task.input(data=SECRET_BOB)
    task.start()

    result = None
    while result is None:
        result = task.result()
    print(api.download(result))
