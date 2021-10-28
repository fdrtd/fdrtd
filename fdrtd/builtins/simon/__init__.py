from fdrtd.builtins.simon.microservice import MicroserviceSimon


def get_microservices():
    return [
        {
            "identifiers": {
                "namespace": "fdrtd",
                "protocol": "Simon",
                "version": "0.3.6"
            },
            "class": MicroserviceSimon,
            "public": ["compute", "get_task", "create_task", "join_task", "peer_to_peer"]
        }
    ]
