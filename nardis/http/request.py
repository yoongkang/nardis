from typing import List, Tuple
from typing_extensions import Protocol

import abc
from nardis.utils import decode_bytes, encode_string
from .utils import parse_cookie, parse_headers, parse_qs


def urlencoded(body: bytes) -> dict:
    return parse_qs(body)


def jsontype(body: bytes) -> dict:
    import json
    return json.loads(body)


class Request:
    handlers = {
        'application/x-www-form-urlencoded': urlencoded,
        'application/json': jsontype,
    }

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
    def content_type(self) -> str:
        return self.headers['content-type']

    @property
    def raw_body(self) -> bytes:
        if self._finished:
            return self._body
        return b''

    @property
    def body(self) -> dict:
        try:
            raw_dict = self.handlers[self.content_type](self._body)
            return {k: (v[0] if len(v) == 1 else v) for k, v in raw_dict.items()}
        except KeyError:
            raise NotImplementedError(
                f"Content type {self.content_type} is not handled yet"
            )
