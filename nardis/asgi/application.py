from .config import get_defaults
from .handlers import ASGIHandler
from typing import Dict


def main(config: dict):
    app_config = {**get_defaults(), **config}
    def application(scope: dict):
        consumers = app_config['consumers']  # type: Dict[str, ASGIHandler]
        return consumers[scope['type']](scope, app_config)
    return application
