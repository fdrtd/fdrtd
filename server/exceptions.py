"""exception handling routines"""

import logging as _logging


def handle_exception(exception):
    """logs an exceptions and returns an error message and error code"""

    if isinstance(exception, ApiError):
        _logging.exception(exception.message)
        return exception.message, exception.statuscode

    _logging.exception(repr(exception))
    return None, 500


class ApiError(Exception):

    """base class of exceptions thrown by the fdrtd API"""

    def __init__(self, statuscode, message):
        super().__init__()

        self.statuscode = statuscode
        self.message = message

    def __str__(self):
        return self.message


class InternalServerError(ApiError):
    """exception child class: internal server error"""

    def __init__(self, message):
        super().__init__(500, f'internal server error: {message}')


class NotAvailable(ApiError):
    """exception child class: not implemented / not available"""

    def __init__(self, missing):
        super().__init__(501, f'not implemented / not available: {missing}')


class MissingParameter(ApiError):
    """exception child class: missing parameter"""

    def __init__(self, missing):
        super().__init__(400, f'missing parameter: {missing}')


class InvalidParameter(ApiError):
    """exception child class: invalid parameter"""

    def __init__(self, parameter, invalid):
        super().__init__(400, f'invalid parameter: {parameter} = {invalid}')


class InvalidIdentifier(ApiError):
    """exception child class: invalid identifier"""

    def __init__(self, identifier, invalid):
        super().__init__(404, f'invalid identifier: {identifier} = {invalid}')


class MicroserviceNotFound(ApiError):
    """this exception is thrown when a microservice does not exist on the bus"""

    def __init__(self, missing):
        super().__init__(404, f'microservice not available: {missing}')


class FunctionNotFound(ApiError):
    """this exception is thrown when a member function of a microservice
       does not exist"""

    def __init__(self, missing):
        super().__init__(404, f'function not available: {missing}')


class FunctionNotPublic(ApiError):
    """this exception is thrown when a member function of a microservice
       exists, but is not public"""

    def __init__(self, missing):
        super().__init__(403, f'function not public: {missing}')
