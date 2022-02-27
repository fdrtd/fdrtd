from fdrtd.builtins.util.kvstorage import KeyValueStorage


def fdrtd_register(registry):

    registry.register(
        {
            "namespace": "fdrtd",
            "plugin": "Util",
            "version": "0.5.3",
            "microservice": "KeyValueStorage"
        },
        KeyValueStorage()
    )
