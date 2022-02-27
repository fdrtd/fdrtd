"""routines to discover plugins and their microservices on server startup"""

import importlib
import pkgutil

import fdrtd.builtins
import fdrtd.plugins


def discover_builtins_and_plugins(registry):
    """discover microservices and classes in fdrtd.builtins and fdrtd.plugins"""

    for namespace_package in [fdrtd.builtins, fdrtd.plugins]:
        for _, name, _ in pkgutil.iter_modules(namespace_package.__path__,
                                               namespace_package.__name__ + "."):
            module = importlib.import_module(name)
            try:
                getattr(module, "fdrtd_register")(registry)
            except AttributeError:
                pass
