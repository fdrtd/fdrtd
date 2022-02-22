from fdrtd.builtins.util.kvstorage import KeyValueStorage


def list_root_objects():
    return [
        {
            "identifiers": {
                "namespace": "fdrtd",
                "plugin": "Util",
                "version": "0.5.2",
                "microservice": "KeyValueStorage"
            },
            "object": KeyValueStorage()
        }
    ]
