import os
from sys import modules
from typing import Container
from unittest import mock

from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject

class APIClient:
    def __init__(self, api_key: str, timeout: int) -> None:
        self.api_key = api_key
        self.timeout = timeout


class Service:
    def __init__(self, api_client: APIClient) -> None:
        self.api_client = api_client


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    api_client = providers.Singleton(
        APIClient,
        api_key=config.api_key,
        timeout=config.timeout
    )

    service = providers.Factory(
        Service,
        api_client=api_client
    )


@inject
def main(service: Service = Provide[Container.service]) -> None:
    print(type(service))


if __name__ == '__main__':
    container = Container()
    container.config.api_key.from_env('API_KEY', required=True)
    container.config.timeout.from_env('TIMEOUT', as_=int, default=5)
    container.wire(modules=[__name__])

    main() # <-- dependency is injected automatically

    with container.api_client.override(mock.Mock()):
        main() # <-- overridden dependency is also injected automatically