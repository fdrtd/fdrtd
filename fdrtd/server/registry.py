from fdrtd.server.discovery import discover_builtins_and_plugins


class Registry:

    def __init__(self):
        self.root_objects = discover_builtins_and_plugins()
