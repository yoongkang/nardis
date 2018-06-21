from typing import List, Tuple
from typing_extensions import Protocol

import abc
from nardis.utils import decode_bytes, encode_string
from .utils import parse_cookie, parse_headers, parse_qs


class Request:
    def __init__(self, scope: dict, body: bytes) -> None:
        self.method = scope['method']
        self.path = scope['path']
        self.headers = parse_headers(scope['headers'])
        self.http_version = scope['http_version']
        self.server = scope['server']
        self._body = body
        self.cookies = parse_cookie(self.headers.get('cookie', ''))
        self.query_string = parse_qs(scope['query_string'])
        self._finished = False
        self._scope = scope
        self.params = {}  # type: dict

    def append_body(self, body: bytes):
        if self._finished:
            raise RuntimeError("Request has already finished")
        self._body += body

    def mark_complete(self):
        self._finished = True

    @property
    def body(self):
        return decode_bytes(self._body)
