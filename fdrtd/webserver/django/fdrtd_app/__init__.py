from fdrtd.server.bus import Bus
from fdrtd.server.discovery import discover_microservices

fdrtd_bus = Bus()
_microservices, _classes = discover_microservices(fdrtd_bus)
fdrtd_bus.set_microservices(_microservices)
fdrtd_bus.set_classes(_classes)

