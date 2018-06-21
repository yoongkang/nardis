from typing import Callable, List, Tuple
from abc import abstractmethod, abstractproperty
from nardis.utils import encode_string
import functools


def check_started(func: Callable) -> Callable:
    @functools.wraps(func)
    def inner(obj, *args, **kwargs):
        if obj._started:
            raise RuntimeError("Response has already started")
        return func(obj, *args, **kwargs)
    return inner


class Response:
    def __init__(self, send: Callable) -> None:
        self._send = send
        self._status = 200
        self._started = False
        self._finished = False
        self.headers = {'content-type': 'text/html'}

    async def send(self, body: str, more: bool=False):
        if not self._started:
            await self.send_head()
        if self._finished:
            raise RuntimeError("Response has already been sent")
        await self._send({
            'type': 'http.response.body',
            'body': encode_string(body),
            'more_body': more,
        })
        self._finished = not more

    def status(self, code: int):
        self._status = code

    def get_headers(self) -> List[Tuple[bytes, bytes]]:
        return [
            (encode_string(k), encode_string(v))
            for k, v in self.headers.items()
        ]

    @check_started
    async def send_head(self) -> None:
        await self._send({
            'type': 'http.response.start',
            'status': self._status,
            'headers': self.get_headers(),
        })
        self._started = True

    @check_started
    async def redirect(self, path: str, code: int=302):
        self.headers['Location'] = path
        await self._send({
            'type': 'http.response.start',
            'status': code,
            'headers': self.get_headers(),
        })
        await self._send({
            "type": "http.response.body",
            "body": b""
        })
