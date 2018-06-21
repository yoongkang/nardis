from typing import Callable
from nardis.http import Request
from .pattern import RegexPattern

import abc


class BaseHTTPMatcher(abc.ABC):
    method = ''

    def __init__(self, path: str, action: Callable, pattern_cls: type=RegexPattern) -> None:
        self.path = path
        self.action = action
        self.pattern = pattern_cls(path)

    def dispatch(self, request, response):
        # if match, parse URL to get (URL) params
        params = self._parse_params(request)
        request.params = params
        return self.action(request, response)

    def _matches_method(self, request) -> bool:
        return self.method == request.method

    def _matches_path(self, request) -> bool:
        return self.pattern.match(request.path)

    def _parse_params(self, request) -> dict:
        return self.pattern.parse(request.path)

    def match(self, request) -> bool:
        return self._matches_method(request) and self._matches_path(request)


class Get(BaseHTTPMatcher):
    method = 'GET'


class Post(BaseHTTPMatcher):
    method = 'POST'
