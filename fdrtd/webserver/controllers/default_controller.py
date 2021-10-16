"""
contains the entry points of the API
"""

from fdrtd.server.bus import get_bus
from fdrtd.server.exceptions import handle_exception


def list_representations():
    """list available server-side objects"""
    try:
        response = get_bus().list_representations()
        return {'type': 'list', 'list': response}, 200  # OK
    except Exception as exception:
        return handle_exception(exception)


def create_representation(body):
    """create a representation"""
    try:
        response = get_bus().create_representation(body)
        return {'type': 'uuid', 'uuid': response}, 200  # OK
    except Exception as exception:
        return handle_exception(exception)


def upload_representation(body):
    """upload an object, and return its representation"""
    try:
        response = get_bus().upload_representation(body)
        return {'type': 'uuid', 'uuid': response}, 200  # OK
    except Exception as exception:
        return handle_exception(exception)


def call_representation(representation_uuid, body):
    """call a server-side object"""
    try:
        response = get_bus().call_representation(representation_uuid, body)
        return {'type': 'uuid', 'uuid': response}, 200  # OK
    except Exception as exception:
        return handle_exception(exception)


def download_representation(representation_uuid):
    """download a serialized version of a server-side object"""
    try:
        response = get_bus().download_representation(representation_uuid)
        return {'type': 'object', 'object': response}, 200  # OK
    except Exception as exception:
        return handle_exception(exception)


def release_representation(representation_uuid):
    """release a representation"""
    try:
        get_bus().release_representation(representation_uuid)
        return {'type': 'none'}, 200  # OK
    except Exception as exception:
        return handle_exception(exception)


def create_attribute(representation_uuid, attribute_name):
    """create a representation of an attribute of a representation"""
    try:
        uuid = get_bus().create_attribute(representation_uuid, attribute_name, public=True)
        return {'type': 'uuid', 'uuid': uuid}, 200  # OK
    except Exception as exception:
        return handle_exception(exception)
