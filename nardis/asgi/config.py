from nardis.routing import default_404, default_500
from .handlers import HTTPHandler


CONSUMERS = {
    'http': HTTPHandler,
}


DEFAULT_CONFIG = {
    'action_404': default_404,
    'action_500': default_500,
    'consumers': CONSUMERS.copy(),
    'routes': [],
}

def get_defaults():
    return DEFAULT_CONFIG.copy()
