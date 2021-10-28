from fdrtd.builtins.util.kvstorage import KeyValueStorage


def get_microservices():
    return [
        {
            "identifiers": {
                "namespace": "fdrtd",
                "plugin": "Util",
                "version": "0.3.0",
                "microservice": "KeyValueStorage"
            },
            "class": KeyValueStorage,
            "public": ["create", "store", "retrieve", "exists", "delete"]
        }
    ]
