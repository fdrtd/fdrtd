from fdrtd.builtins.util.kvstorage import KeyValueStorage


def list_root_objects():
    return [
        {
            "identifiers": {
                "namespace": "fdrtd",
                "plugin": "Util",
                "version": "0.3.0",
                "microservice": "KeyValueStorage"
            },
            "object": KeyValueStorage()
        }
    ]
