from fdrtd.builtins.sync.barrier import Barrier
from fdrtd.builtins.sync.broadcast import Broadcast


def get_microservices():
    return [
        {
            "identifiers": {
                "namespace": "fdrtd",
                "plugin": "Sync",
                "version": "0.3.0",
                "microservice": "Barrier"
            },
            "class": Barrier,
            "public": ["create", "delete"]
        },
        {
            "identifiers": {
                "namespace": "fdrtd",
                "plugin": "Sync",
                "version": "0.3.0",
                "microservice": "Broadcast"
            },
            "class": Broadcast,
            "public": ["create", "send", "receive", "delete"]
        }
    ]
