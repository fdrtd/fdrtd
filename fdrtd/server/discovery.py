"""routines to discover plugins and their microservices on server startup"""

import uuid as _uuid
import importlib
import pkgutil

import fdrtd.builtins
import fdrtd.plugins


def discover_builtins_and_plugins():
    """discover microservices and classes in fdrtd.builtins and fdrtd.plugins"""

    root_objects = {}

    for namespace_package in [fdrtd.builtins, fdrtd.plugins]:
        for _, name, _ in pkgutil.iter_modules(namespace_package.__path__,
                                               namespace_package.__name__ + "."):
            module = importlib.import_module(name)
            try:
                for item in getattr(module, "list_root_objects")():
                    uuid = str(_uuid.uuid4())
                    root_objects[uuid] = item
            except AttributeError:
                pass

    return root_objects
