from typing import Callable
from typing_extensions import Protocol
from nardis.http import Request, Response
from .pattern import RegexPattern

import abc


class Matcher(Protocol):
    @abc.abstractmethod
    def __init__(self, path: str, action: Callable, pattern_cls: type) -> None:
        pass

    @abc.abstractmethod
    def match(self, scope: dict) -> bool:
        pass


class BaseHTTPMatcher(abc.ABC):
    method = ''

    def __init__(self, path: str, action: Callable, pattern_cls: type=RegexPattern) -> None:
        self.path = path
        self.action = action
        self.pattern = pattern_cls(path)

    def dispatch(self, request: Request, response: Response):
        # if match, parse URL to get (URL) params
        params = self._parse_params(request)
        request.params = params
        return self.action(request, response)

    def _matches_method(self, scope: dict) -> bool:
        return self.method == scope['method']

    def _matches_path(self, scope: dict) -> bool:
        return self.pattern.match(scope['path'])

    def _parse_params(self, request: Request) -> dict:
        return self.pattern.parse(request.path)

    def match(self, scope: dict) -> bool:
        return (
            scope['type'] == 'http' and
            self._matches_method(scope) and
            self._matches_path(scope)
        )


class Get(BaseHTTPMatcher):
    method = 'GET'


class Post(BaseHTTPMatcher):
    method = 'POST'


class WebSocketsMatcher:
    def __init__(self, path: str, action: Callable, pattern_cls: type=RegexPattern) -> None:
        self.path = path
        self.action = action

    def match(self, scope: dict) -> bool:
        return (
            scope['type'] == 'websocket' and
            scope['path'] == self.path
        )

    def dispatch(self, receive, send):
        return self.action(receive, send)
