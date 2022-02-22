from fdrtd.builtins.sync.barrier import Barrier
from fdrtd.builtins.sync.broadcast import Broadcast


def get_classes():
    return [
        {
            "identifiers": {
                "namespace": "fdrtd",
                "plugin": "Sync",
                "version": "0.3.0",
                "microservice": "Barrier"
            },
            "class": Barrier()
        },
        {
            "identifiers": {
                "namespace": "fdrtd",
                "plugin": "Sync",
                "version": "0.3.0",
                "microservice": "Broadcast"
            },
            "class": Broadcast()
        }
    ]
