from fdrtd.builtins.util.kvstorage import KeyValueStorage


def get_classes():
    return [
        {
            "identifiers": {
                "namespace": "fdrtd",
                "plugin": "Util",
                "version": "0.3.0",
                "microservice": "KeyValueStorage"
            },
            "class": KeyValueStorage()
        }
    ]
