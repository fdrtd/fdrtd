from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


import fdrtd.webserver.django.fdrtd_app
from fdrtd.server.exceptions import handle_exception


@csrf_exempt
def path_representations(request):
    """route requests to /representations"""
    if request.method == 'GET':
        return list_representations()
    if request.method == 'POST':
        return create_representation(json.loads(request.body))
    if request.method == 'PUT':
        return upload_representation(json.loads(request.body))


@csrf_exempt
def path_representation_uuid(request, uuid):
    """route requests to /representation/<uuid>"""
    if request.method == 'PATCH':
        return call_representation(str(uuid), json.loads(request.body))
    if request.method == 'GET':
        return download_representation(str(uuid))
    if request.method == 'DELETE':
        return release_representation(str(uuid))


@csrf_exempt
def path_representation_uuid_name(request, uuid, name):
    """route requests to /representation/<uuid>/<name>"""
    if request.method == 'GET':
        return create_attribute(str(uuid), name)


def get_bus():
    """get the singleton bus of the server application"""
    return fdrtd.webserver.django.fdrtd_app.fdrtd_bus


def list_representations():
    """list available server-side objects"""
    try:
        response = get_bus().list_representations()
        return JsonResponse({'type': 'list', 'list': response})
    except Exception as exception:
        message, status = handle_exception(exception)
        return JsonResponse({'message': message}, status=status)


def create_representation(body):
    """create a representation"""
    try:
        response = get_bus().create_representation(body)
        return JsonResponse({'type': 'uuid', 'uuid': response})
    except Exception as exception:
        message, status = handle_exception(exception)
        return JsonResponse({'message': message}, status=status)


def upload_representation(body):
    """upload an object, and return its representation"""
    try:
        response = get_bus().upload_representation(body)
        return JsonResponse({'type': 'uuid', 'uuid': response})
    except Exception as exception:
        message, status = handle_exception(exception)
        return JsonResponse({'message': message}, status=status)


def call_representation(representation_uuid, body):
    """call a server-side object"""
    try:
        response = get_bus().call_representation(representation_uuid, body)
        if response is None:
            return JsonResponse({'type': 'none'})
        return JsonResponse({'type': 'uuid', 'uuid': response})
    except Exception as exception:
        message, status = handle_exception(exception)
        return JsonResponse({'message': message}, status=status)


def download_representation(representation_uuid):
    """download a serialized version of a server-side object"""
    try:
        response = get_bus().download_representation(representation_uuid)
        return JsonResponse({'type': 'object', 'object': response})
    except Exception as exception:
        message, status = handle_exception(exception)
        return JsonResponse({'message': message}, status=status)


def release_representation(representation_uuid):
    """release a representation"""
    try:
        get_bus().release_representation(representation_uuid)
        return JsonResponse({'type': 'none'})
    except Exception as exception:
        message, status = handle_exception(exception)
        return JsonResponse({'message': message}, status=status)


def create_attribute(representation_uuid, attribute_name):
    """create a representation of an attribute of a representation"""
    try:
        uuid = get_bus().create_attribute(representation_uuid, attribute_name, public=True)
        return JsonResponse({'type': 'uuid', 'uuid': uuid})
    except Exception as exception:
        message, status = handle_exception(exception)
        return JsonResponse({'message': message}, status=status)
