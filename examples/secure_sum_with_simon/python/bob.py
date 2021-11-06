"""
secure sum example with Simon

three fdrtd servers are needed for this example.
one for each of Alice, Bob, and Charlie.
and an additional one for invitations and synchronizing.
the easiest way is to run them all on localhost:

    pip install fdrtd
    python -m fdrtd.webserver --port=55501 &
    python -m fdrtd.webserver --port=55502 &
    python -m fdrtd.webserver --port=55503 &

then, the three scripts of Alice, Bob, and Charlie may be executed simultaneously.
"""


import fdrtd.clients.python
import shared


SECRET_BOB = 16.0
NETWORK_BOB = {**shared.NETWORK, 'myself': 1}  # Bob is no. 1 out of 0, 1, 2.


if __name__ == "__main__":

    api = fdrtd.clients.python.Api(shared.URL_BOB)
    microservice = api.create(protocol="Simon")
    result = microservice.compute(microprotocol="BasicSum",
                                  data=SECRET_BOB,
                                  network=NETWORK_BOB,
                                  tokens=shared.TOKENS)
    print(api.download(result))
