import re
from nardis.http import Request, Response
from nardis.utils import encode_string
from nardis.routing import BaseHTTPMatcher
from typing import List


class HTTPHandler:
    def __init__(self, scope: dict, matchers: List[BaseHTTPMatcher]) -> None:
        self.scope = scope
        self.request = Request(scope, b'')
        self.matchers = matchers  # type: List[BaseHTTPMatcher]

    async def wait_request(self, receive, send):
        while True:
            msg = await receive()
            if msg['type'] == 'http.disconnect':
                break
            self.request.append_body(msg['body'])
            if not msg.get('more_body', False):
                self.request.mark_complete()
                break

    async def __call__(self, receive, send):
        await self.wait_request(receive, send)
        resp = Response(send)
        for matcher in self.matchers:
            if matcher.match(self.request):
                await matcher.dispatch(self.request, resp)
                break
        else:
            resp.status(404)
            await resp.send("not found")


CONSUMERS = {
    'http': HTTPHandler,
}


def main(matchers: list):
    def application(scope: dict):
        return CONSUMERS[scope['type']](scope, matchers)
    return application