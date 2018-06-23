import re
import abc
from nardis.http import Request, Response
from nardis.utils import encode_string
from nardis.routing import Matcher, BaseHTTPMatcher
from typing import List, Callable, Coroutine
from typing_extensions import Protocol
from nardis.routing import default_404, default_500

import traceback
import functools


def rescue(func):
    """
    Decorator to show a 500 page.
    """
    @functools.wraps(func)
    async def inner(obj, receive, send):
        try:
            await func(obj, receive, send)
        except Exception as e:  # catch all
            traceback.print_exc()
            action = obj.config.get('action_500')
            await action(obj.request, Response(send))
    return inner


class ASGIHandler(Protocol):
    @abc.abstractmethod
    def __init__(self, scope: dict, config: dict) -> None:
        pass

    @abc.abstractmethod
    async def __call__(self, receive, send):
        pass


class HTTPHandler:
    def __init__(self, scope: dict, config: dict) -> None:
        self.scope = scope
        self.request = Request(scope, b'')
        self.config = config
        self.matchers = config['routes']  # List[Matcher]

    async def wait_request(self, receive, send):
        while True:
            msg = await receive()
            if msg['type'] == 'http.disconnect':
                break
            self.request.append_body(msg['body'])
            if not msg.get('more_body', False):
                self.request.mark_complete()
                break

    @rescue
    async def __call__(self, receive, send):
        await self.wait_request(receive, send)
        resp = Response(send)
        for matcher in self.matchers:
            if matcher.match(self.scope):
                await matcher.dispatch(self.request, resp)
                break
        else:
            action_404 = self.config.get('action_404')
            await action_404(self.request, resp)
