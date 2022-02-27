from fdrtd.builtins.sync.barrier import Barrier
from fdrtd.builtins.sync.broadcast import Broadcast


def fdrtd_register(registry):

    registry.register(
        {
            "namespace": "fdrtd",
            "plugin": "Sync",
            "version": "0.5.3",
            "microservice": "Barrier"
        },
        Barrier()
    )

    registry.register(
        {
            "namespace": "fdrtd",
            "plugin": "Sync",
            "version": "0.5.3",
            "microservice": "Broadcast"
        },
        Broadcast()
    )
