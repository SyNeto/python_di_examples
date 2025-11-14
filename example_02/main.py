"""
Example 02 - Implementation with Dependency Injector Framework

This example shows how to use the 'dependency-injector' framework to
automatically manage your application's dependencies.

Key concepts demonstrated:

1. Container:
   - Class that declares and manages all dependencies
   - Centralizes the dependency graph configuration
   - Facilitates testing by allowing dependency overrides

2. Providers:
   - Singleton: Creates ONE SINGLE shared instance (e.g., DB connections, configs)
   - Factory: Creates A NEW instance each time it's requested (e.g., requests)
   - Configuration: Manages configuration from env vars, files, etc.

3. @inject decorator:
   - Marks functions that will receive dependencies automatically
   - Allows automatic injection without manually passing parameters

4. Dependency override:
   - Allows replacing real dependencies with mocks for testing
   - Useful for isolating components during tests

Compared to example_01/main_di.py, this approach:
- Eliminates duplicated manual assembly code
- Centralizes dependency configuration
- Facilitates testing with overrides
- Scales better in large applications

Documentation: https://python-dependency-injector.ets-labs.org/
"""
import os
from sys import modules
from unittest import mock

from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject


class APIClient:
    """
    API client that requires external configuration.

    This is the same class from example_01, but now it will be managed
    by the DI container instead of being manually assembled.

    Args:
        api_key: API key for authentication
        timeout: Timeout in seconds for requests
    """

    def __init__(self, api_key: str, timeout: int) -> None:
        self.api_key = api_key
        self.timeout = timeout


class Service:
    """
    Service that depends on APIClient.

    Args:
        api_client: API client for making requests
    """

    def __init__(self, api_client: APIClient) -> None:
        self.api_client = api_client


class Container(containers.DeclarativeContainer):
    """
    Dependency Injection container.

    This container declares all application dependencies and how
    they should be constructed. Defines the complete dependency graph.

    Attributes:
        config: Configuration provider that reads from environment variables
        api_client: Singleton provider that creates ONE shared instance of APIClient
        service: Factory provider that creates NEW instances of Service when requested
    """

    # Configuration provider: manages configuration from env vars
    config = providers.Configuration()

    # Singleton provider: ONE SINGLE shared instance
    # Useful for expensive resources like DB connections, configs, HTTP clients
    api_client = providers.Singleton(
        APIClient,
        api_key=config.api_key,
        timeout=config.timeout
    )

    # Factory provider: NEW instance each time
    # Useful for stateful objects that shouldn't be shared
    service = providers.Factory(
        Service,
        api_client=api_client
    )


@inject
def main(service: Service = Provide[Container.service]) -> None:
    """
    Main function with automatic dependency injection.

    The @inject decorator allows the container to automatically inject
    the 'service' dependency without having to pass it manually.

    Args:
        service: Service automatically injected by the container.
                 Provide[Container.service] indicates WHICH dependency to inject.
    """
    print(type(service))


if __name__ == '__main__':
    # 1. Create the container
    container = Container()

    # 2. Configure from environment variables
    container.config.api_key.from_env('API_KEY', required=True)
    container.config.timeout.from_env('TIMEOUT', as_=int, default=5)

    # 3. Wire (connect) the container with this module
    # This activates automatic injection for functions decorated with @inject
    container.wire(modules=[__name__])

    # 4. Call main() without passing parameters
    # The @inject decorator automatically injects the dependency
    main()

    # 5. Demonstration of override for testing
    # Replace real api_client with a Mock for testing
    with container.api_client.override(mock.Mock()):
        main()  # Now uses the mock instead of the real APIClient
