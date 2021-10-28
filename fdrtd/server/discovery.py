"""routines to discover plugins and their microservices on server startup"""

import uuid as _uuid
import importlib
import pkgutil

import fdrtd.builtins
import fdrtd.plugins


def discover_microservices(bus):

    microservices = {}
    classes = {}

    for namespace_package in [fdrtd.builtins, fdrtd.plugins]:
        for finder, name, ispkg in pkgutil.iter_modules(namespace_package.__path__, namespace_package.__name__ + "."):
            module = importlib.import_module(name)
            try:
                for item in getattr(module, "get_microservices")():
                    uuid = str(_uuid.uuid4())
                    instance = item['class'](bus, uuid)
                    public = instance.make_public()
                    if 'public' in item:
                        public.update({function: getattr(instance, function)
                                       for function in item['public']})
                    private = {}
                    for attr in dir(instance):
                        if ('__' not in attr) \
                                and (callable(getattr(instance, attr))) \
                                and (attr not in public):
                            private[attr] = getattr(instance, attr)
                    microservices[uuid] = {
                        **item,
                        'instance': instance,
                        'public': public,
                        'private': private
                    }
            except AttributeError:
                pass
            try:
                for item in getattr(module, "get_classes")():
                    uuid = str(_uuid.uuid4())
                    classes[uuid] = {**item, 'instance': item['class']()}
            except AttributeError:
                pass
    return microservices, classes
