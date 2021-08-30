"""routines to discover plugins and their microservices on server startup"""

import importlib.util as _importlibutil
import os as _os
import json as _json
import uuid as _uuid


def import_microservice_python(root, bus, microservice, uuid):
    """import a microservice from a python module"""
    spec = _importlibutil.spec_from_file_location(
        microservice['classname'],
        root + "/" + microservice['classfile'])
    mod = _importlibutil.module_from_spec(spec)
    spec.loader.exec_module(mod)
    cls = getattr(mod, microservice['classname'], None)
    instance = cls(bus, uuid)
    public = instance.make_public()
    if 'public' in microservice:
        public.update({function: getattr(instance, function)
                       for function in microservice['public']})
    private = {}
    for attr in dir(instance):
        if ('__' not in attr) \
                and (callable(getattr(instance, attr))) \
                and (attr not in public):
            private[attr] = getattr(instance, attr)
    return {
        **microservice,
        'class': cls,
        'instance': instance,
        'public': public,
        'private': private
    }


def discover_microservices(path, bus):
    """scan for plugin manifests, and return a dictionary of microservices"""
    microservices = {}
    for root, _, files in _os.walk(_os.path.abspath(path)):
        if "fdrtd_plugin.json" in files:
            with open(root + "/fdrtd_plugin.json", encoding='utf-8') as file:
                manifest = _json.load(file)
                for microservice in manifest['microservices']:
                    if microservice['language'] == 'Python':
                        uuid = str(_uuid.uuid4())
                        microservices[uuid] = import_microservice_python(
                            root, bus, microservice, uuid)
                    # TODO: support other languages
    return microservices
