from fdrtd.server.bus import get_bus
from fdrtd.server.callback import Callback
from fdrtd.server.exceptions import handle_exception


def list_microservices():
    try:
        response = get_bus().list_microservices()
        return response, 200  # OK
    except Exception as e:
        return handle_exception(e)


def select_microservice(body):
    try:
        response = get_bus().select_microservice(body)
        return response, 202  # Accepted
    except Exception as e:
        return handle_exception(e)


def call_microservice(body):
    try:
        result = get_bus().call_microservice(body['handle'],
                                             body['function'],
                                             body['parameters'],
                                             body.get('callback', None),
                                             public=True)
        if result is None:
            return None, 204  # No Content
        if isinstance(result, Callback):
            return result, 202 if result['callback'] is None else 201
        return result, 200
    except Exception as e:
        return handle_exception(e)
