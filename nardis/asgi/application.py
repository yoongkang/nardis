from .config import get_defaults


def main(config: dict):
    app_config = {**get_defaults(), **config}
    def application(scope: dict):
        consumers = app_config['consumers']
        return consumers[scope['type']](scope, app_config)
    return application
