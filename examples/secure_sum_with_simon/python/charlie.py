"""
secure sum example with Simon

three fdrtd servers are needed for this example.
one for each of Alice, Bob, and Charlie.
and an additional one for invitations and synchronizing.
the easiest way is to run them all on localhost:

    pip install fdrtd
    pip install fdrtd-simon
    python -m fdrtd.webserver --port=55501 &
    python -m fdrtd.webserver --port=55502 &
    python -m fdrtd.webserver --port=55503 &

then, the three scripts of Alice, Bob, and Charlie may be executed simultaneously.
"""


import fdrtd.client
import shared


SECRET_CHARLIE = 99.0
NETWORK_CHARLIE = {**shared.NETWORK, 'myself': 2}  # Charlie is no. 2 out of 0, 1, 2.


if __name__ == "__main__":

    api = fdrtd.client.Api(shared.URL_CHARLIE)
    microservice = api.create(protocol="Simon")
    result = microservice.compute(microprotocol="SecureSum",
                                  data=SECRET_CHARLIE,
                                  network=NETWORK_CHARLIE,
                                  tokens=shared.TOKENS)
    print(api.download(result))
