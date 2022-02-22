from fdrtd.builtins.sync.barrier import Barrier
from fdrtd.builtins.sync.broadcast import Broadcast


def list_root_objects():
    return [
        {
            "identifiers": {
                "namespace": "fdrtd",
                "plugin": "Sync",
                "version": "0.3.0",
                "microservice": "Barrier"
            },
            "object": Barrier()
        },
        {
            "identifiers": {
                "namespace": "fdrtd",
                "plugin": "Sync",
                "version": "0.3.0",
                "microservice": "Broadcast"
            },
            "object": Broadcast()
        }
    ]
