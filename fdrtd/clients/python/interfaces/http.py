"""
contains class HttpInterface
"""

import datetime as _datetime
import logging as _logging
import requests as _requests
import urllib3 as _urllib3


class HttpInterface:

    """
    HttpInterface communicates through HTTP or HTTPS with the server
    """

    # enable the following line if SSL verification fails on e.g. localhost
    _urllib3.disable_warnings(category=_urllib3.exceptions.InsecureRequestWarning)

    # enable the following line if SSL verification fails on Android devices
    _urllib3.util.ssl_.DEFAULT_CIPHERS =\
        "TLS13-CHACHA20-POLY1305-SHA256:TLS13-AES-128-GCM-SHA256:" \
        "TLS13-AES-256-GCM-SHA384:ECDHE:!COMPLEMENTOFDEFAULT "

    # set to False to disable, set to True to enable SSL verification
    ssl_verify = False

    def __init__(self, root):
        self.root = root

    def post(self, *path, body=None):
        """do a POST request"""
        return self._call(_requests.post, *path, body=body, method="POST")

    def put(self, *path, body=None):
        """do a PUT request"""
        return self._call(_requests.put, *path, body=body, method="PUT")

    def patch(self, *path, body=None):
        """do a PATCH request"""
        return self._call(_requests.patch, *path, body=body, method="PATCH")

    def get(self, *path):
        """do a GET request"""
        return self._call(_requests.get, *path, method="GET")

    def delete(self, *path):
        """do a DELETE request"""
        return self._call(_requests.delete, *path, method="DELETE")

    def _call(self, hook, *path, body=None, method="-"):

        url = self.root
        for item in path:
            if item[0] == '/':
                url = url + item
            else:
                url = url + '/' + item

        logger = _logging.getLogger(__name__)

        logger.debug('Sending request: %s %s %s', method, url, body)
        response = hook(url=url, json={} if body is None else body, verify=HttpInterface.ssl_verify)
        logger.debug('Receiving response: %d %s', response.status_code, response.text)

        if response.status_code not in [200, 201, 202, 204]:
            message = HttpInterface._formatted_line(
                method, url, response.status_code, response.text)
            logger.error(message)
            raise Exception(message)

        message = HttpInterface._formatted_line(
            method, url, response.status_code)
        logger.info(message)

        return None if response.text == '' else response.json(), response.status_code

    @staticmethod
    def _formatted_line(method="-", uri="-", status="-", comment="-"):
        """log format according to W3C Working Draft WD-logfile-960323"""
        date = _datetime.date.today().strftime("%Y-%m-%d")
        time = _datetime.datetime.now().strftime("%H:%M:%S")
        human_readable = HttpInterface._human_readable(status)
        return f'{date}\t{time}\t{method}\t{uri}\t{status}\t{human_readable}\t{comment}'

    @staticmethod
    def _human_readable(status):
        return {
            100: 'Continue',
            101: 'Switching Protocols',
            200: 'OK',
            201: 'Created',
            202: 'Accepted',
            203: 'Non-Authoritative Information',
            204: 'No Content',
            205: 'Reset Content',
            206: 'Partial Content',
            300: 'Multiple Choices',
            301: 'Moved Permanently',
            302: 'Found',
            303: 'See Other',
            304: 'Not Modified',
            305: 'Use Proxy',
            307: 'Temporary Redirect',
            400: 'Bad Request',
            401: 'Unauthorized',
            402: 'Payment Required',
            403: 'Forbidden',
            404: 'Not Found',
            405: 'Method Not Allowed',
            406: 'Not Acceptable',
            407: 'Proxy Authentication Required',
            408: 'Request Timeout',
            409: 'Conflict',
            410: 'Gone',
            411: 'Length Required',
            412: 'Precondition Failed',
            413: 'Payload Too Large',
            414: 'URI Too Long',
            415: 'Unsupported Media Type',
            416: 'Range Not Satisfiable',
            417: 'Expectation Failed',
            426: 'Upgrade Required',
            500: 'Internal Server Error',
            501: 'Not Implemented',
            502: 'Bad Gateway',
            503: 'Service Unavailable',
            504: 'Gateway Timeout',
            505: 'HTTP Version Not Supported'
        }.get(status, 'n/a')
