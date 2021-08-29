#!/usr/bin/env python3

import connexion
import sys
import os
import waitress

from fdrtd.webserver.encoder import JSONEncoder
from flask import current_app

from fdrtd.server.discovery import discover_microservices
from fdrtd.server.bus import Bus


def main():

    # enable the following line to log endpoint traffic
    # logging.basicConfig(level=logging.INFO)

    port = 8080
    plugin_directory = "fdrtd"
    sys.path.append(os.path.abspath("fdrtd"))
    for arg in sys.argv:
        if arg[:7] == "--port=":
            port = int(arg[7:])
        if arg[:19] == "--plugin_directory=":
            plugin_directory = arg[19:]
            sys.path.append(os.path.abspath(plugin_directory))
    
    bus = Bus()
    microservices = discover_microservices(plugin_directory, bus)
    bus.set_microservices(microservices)

    app = connexion.App(__name__, specification_dir='openapi/')
    app.app.json_encoder = JSONEncoder
    app.add_api('openapi.yaml',
                arguments={'title': 'fdrtd'},
                pythonic_params=True)

    with app.app.app_context():
        current_app.bus = bus

    waitress.serve(app, host="0.0.0.0", port=port)


if __name__ == '__main__':
    main()
