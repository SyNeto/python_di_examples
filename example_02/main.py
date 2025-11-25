"""
Example 02 - Implementation with Dependency Injector Framework.

This example shows how to use the 'dependency-injector' framework to
automatically manage your application's dependencies, solving the
manual assembly limitations from example_01.

Key concepts demonstrated:
    1. **Container**: Class that declares and manages all dependencies.
       Centralizes the dependency graph configuration in one place.

    2. **Providers**: Define HOW dependencies are created:
       - Singleton: ONE shared instance (DB connections, configs).
       - Factory: NEW instance each time (request handlers, transactions).
       - Configuration: Reads from env vars, files, dicts.

    3. **@inject decorator**: Marks functions for automatic injection.
       No need to manually pass dependencies.

    4. **Override**: Replace real dependencies with mocks for testing.
       Essential for isolated unit tests.

Advantages over manual DI (example_01):
    - No duplicated assembly code.
    - Centralized configuration.
    - Built-in testing support with overrides.
    - Automatic lifecycle management.
    - Scales well to large applications.

Example:
    >>> # Normal usage - dependencies are auto-injected
    >>> container = Container()
    >>> container.config.api_key.from_value('my-key')
    >>> container.config.timeout.from_value(30)
    >>> container.wire(modules=[__name__])
    >>> main()  # Service is automatically injected!

    >>> # Testing - override with mocks
    >>> from unittest.mock import Mock
    >>> with container.api_client.override(Mock()):
    ...     main()  # Uses mock instead of real client

See Also:
    - example_01/main_di.py: Manual DI without framework
    - interfaces.protocols: Protocol definitions
    - https://python-dependency-injector.ets-labs.org/
"""
import os
import sys
from unittest import mock

# Add project root to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject

from interfaces import APIClientProtocol


class APIClient:
    """API client managed by the DI container.

    This is the same decoupled class from example_01, but now its lifecycle
    is managed by the DI container instead of manual assembly.

    The container handles:
        - Reading configuration from environment.
        - Creating the instance at the right time.
        - Sharing the instance (Singleton) or creating new ones (Factory).
        - Replacing with mocks during tests.

    Attributes:
        api_key: API key for authentication.
        timeout: Timeout in seconds for requests.

    Example:
        >>> # Created by container, not manually
        >>> container = Container()
        >>> container.config.api_key.from_value('key')
        >>> container.config.timeout.from_value(30)
        >>> client = container.api_client()
        >>> client.timeout
        30
    """

    def __init__(self, api_key: str, timeout: int) -> None:
        """Initialize client with configuration from container.

        Args:
            api_key: API key for authentication.
            timeout: Timeout in seconds for requests.

        Note:
            You typically don't call this directly. The container
            calls it when the dependency is needed.
        """
        self.api_key = api_key
        self.timeout = timeout


class Service:
    """Service with dependencies managed by the container.

    The container automatically injects the APIClient when creating
    this service. You don't need to manually wire dependencies.

    Attributes:
        api_client: API client instance, automatically injected.

    Example:
        >>> container = Container()
        >>> # ... configure container ...
        >>> service = container.service()
        >>> type(service.api_client)
        <class '__main__.APIClient'>
    """

    def __init__(self, api_client: APIClientProtocol) -> None:
        """Initialize service with injected API client.

        Args:
            api_client: API client, automatically provided by container.
        """
        self.api_client = api_client


class Container(containers.DeclarativeContainer):
    """Dependency Injection container for the application.

    This container declares all application dependencies and defines
    how they should be constructed. It's the single source of truth
    for the dependency graph.

    The container pattern provides:
        - Centralized configuration.
        - Lazy instantiation (dependencies created when needed).
        - Lifecycle management (Singleton vs Factory).
        - Easy testing with override().

    Attributes:
        config: Configuration provider for environment variables.
        api_client: Singleton provider for APIClient.
            ONE instance shared across the application.
        service: Factory provider for Service.
            NEW instance each time it's requested.

    Example:
        >>> container = Container()
        >>> container.config.api_key.from_env('API_KEY')
        >>> container.config.timeout.from_env('TIMEOUT', as_=int)
        >>>
        >>> # Get a service (api_client is auto-injected)
        >>> service = container.service()
        >>> type(service.api_client)
        <class '__main__.APIClient'>

    Note:
        Singleton vs Factory:
        - Use Singleton for expensive resources (DB connections, HTTP clients).
        - Use Factory for stateful objects that shouldn't be shared.
    """

    # Configuration provider
    # ======================
    # Reads configuration from environment variables, files, or dicts.
    # Supports type conversion and default values.
    config = providers.Configuration()

    # Singleton provider
    # ==================
    # Creates ONE SINGLE shared instance across the application.
    # The instance is created lazily (on first access) and cached.
    #
    # Use for:
    #   - Database connections (expensive to create)
    #   - HTTP clients (connection pooling)
    #   - Configuration objects (read once, use everywhere)
    api_client = providers.Singleton(
        APIClient,
        api_key=config.api_key,
        timeout=config.timeout
    )

    # Factory provider
    # ================
    # Creates a NEW instance each time it's requested.
    # Dependencies (like api_client) are resolved automatically.
    #
    # Use for:
    #   - Request handlers (isolated per request)
    #   - Transaction objects (shouldn't share state)
    #   - Anything that accumulates state over time
    service = providers.Factory(
        Service,
        api_client=api_client
    )


@inject
def main(service: Service = Provide[Container.service]) -> None:
    """Entry point with automatic dependency injection.

    The @inject decorator enables automatic injection from the container.
    The default value Provide[Container.service] tells the injector
    WHICH dependency to inject.

    How it works:
        1. Container.wire() connects the container to this module.
        2. When main() is called without arguments, @inject kicks in.
        3. The container resolves Container.service and passes it.
        4. The Service is created with its APIClient automatically.

    Args:
        service: Service automatically injected by the container.
            Provide[Container.service] specifies the provider to use.

    Example:
        >>> container = Container()
        >>> container.config.api_key.from_value('test')
        >>> container.config.timeout.from_value(30)
        >>> container.wire(modules=[__name__])
        >>> main()  # No arguments needed!
        <class '__main__.Service'>
    """
    print(type(service))


if __name__ == '__main__':
    # Step 1: Create the container
    # ============================
    # The container is the central registry for all dependencies.
    container = Container()

    # Step 2: Configure from environment variables
    # =============================================
    # The Configuration provider can read from multiple sources:
    #   - from_env(): Environment variables
    #   - from_yaml(): YAML files
    #   - from_dict(): Python dictionaries
    #
    # Options:
    #   - required=True: Raise error if not set
    #   - as_=int: Type conversion
    #   - default=5: Fallback value
    container.config.api_key.from_env('API_KEY', required=True)
    container.config.timeout.from_env('TIMEOUT', as_=int, default=5)

    # Step 3: Wire the container to this module
    # =========================================
    # Wiring connects the container to functions decorated with @inject.
    # After wiring, those functions can receive dependencies automatically.
    container.wire(modules=[__name__])

    # Step 4: Call main() without parameters
    # ======================================
    # The @inject decorator automatically resolves dependencies.
    # You don't need to manually create or pass anything.
    main()

    # Step 5: Demonstration of override for testing
    # ==============================================
    # The override() context manager temporarily replaces a dependency.
    # This is essential for unit testing - you can inject mocks!
    #
    # Benefits:
    #   - No need to modify source code for testing
    #   - Isolate components under test
    #   - Control behavior of dependencies
    with container.api_client.override(mock.Mock()):
        main()  # Now uses the mock instead of real APIClient
