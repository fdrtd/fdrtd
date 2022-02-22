from fdrtd.builtins.sync.barrier import Barrier
from fdrtd.builtins.sync.broadcast import Broadcast


def list_root_objects():
    return [
        {
            "identifiers": {
                "namespace": "fdrtd",
                "plugin": "Sync",
                "version": "0.5.2",
                "microservice": "Barrier"
            },
            "object": Barrier()
        },
        {
            "identifiers": {
                "namespace": "fdrtd",
                "plugin": "Sync",
                "version": "0.5.2",
                "microservice": "Broadcast"
            },
            "object": Broadcast()
        }
    ]
