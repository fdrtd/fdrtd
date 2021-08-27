import importlib.util as _importlibutil
import os as _os
import json as _json
import uuid as _uuid


def discover_microservices(path, bus):

    microservices = {}
    for root, _, files in _os.walk(_os.path.abspath(path)):
        if "fdrtd_plugin.json" in files:
            with open(root + "/fdrtd_plugin.json") as file:
                manifest = _json.load(file)
                for ms in manifest['microservices']:
                    if ms['language'] != 'Python':
                        continue  # TODO: support other languages
                    spec = _importlibutil.spec_from_file_location(ms['classname'], root + "/" + ms['classfile'])
                    mod = _importlibutil.module_from_spec(spec)
                    spec.loader.exec_module(mod)
                    uuid = str(_uuid.uuid4())
                    cls = getattr(mod, ms['classname'], None)
                    microservices[uuid] = {
                        **ms,
                        'class': cls,
                        'instance': cls(bus, uuid),
                        'public': ms['public']
                    }
    return microservices
