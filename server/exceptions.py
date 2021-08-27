import logging as _logging


def handle_exception(e):

    if isinstance(e, ApiError):
        _logging.exception(e.message)
        return e.message, e.statuscode

    _logging.exception(repr(e))
    return None, 500


class ApiError(Exception):

    def __init__(self, statuscode, message):
        self.statuscode = statuscode
        self.message = message

    def __str__(self):
        return self.message


class InternalServerError(ApiError):

    def __init__(self, message):
        super().__init__(500, f'internal server error: {message}')


class NotAvailable(ApiError):

    def __init__(self, missing):
        super().__init__(501, f'not implemented / not available: {missing}')


class MissingParameter(ApiError):

    def __init__(self, missing):
        super().__init__(400, f'missing parameter: {missing}')


class InvalidParameter(ApiError):

    def __init__(self, parameter, invalid):
        super().__init__(400, f'invalid parameter: {parameter} = {invalid}')


class InvalidIdentifier(ApiError):

    def __init__(self, identifier, invalid):
        super().__init__(404, f'invalid identifier: {identifier} = {invalid}')


class MicroserviceNotFound(ApiError):

    def __init__(self, missing):
        super().__init__(404, f'microservice not available: {missing}')


class FunctionNotFound(ApiError):

    def __init__(self, missing):
        super().__init__(404, f'function not available: {missing}')


class FunctionNotPublic(ApiError):

    def __init__(self, missing):
        super().__init__(403, f'function not public: {missing}')
