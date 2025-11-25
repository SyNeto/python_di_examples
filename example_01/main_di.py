"""
Example 01 - Decoupled code prepared for Dependency Injection.

This example shows how to refactor the code from main_before.py to
prepare it for Dependency Injection. The key changes are:

Improvements implemented:
    1. **Constructor injection**: Classes receive dependencies as parameters.
    2. **No internal creation**: Classes don't create their own dependencies.
    3. **Single assembly point**: All wiring happens in one place (__main__).
    4. **Easy to test**: Can inject mocks without modifying source code.

Design principles applied:
    - Dependency Inversion Principle (DIP): Depend on abstractions, not concretions.
    - Single Responsibility: Classes do one thing, assembly is separate.
    - Explicit dependencies: All dependencies are visible in constructors.

Limitation:
    The manual assembly code (lines 80-84) works but is prone to duplication
    and becomes complex in large applications. For the solution, see example_02
    which uses a DI container.

Example:
    >>> from unittest.mock import Mock
    >>> # Easy to test with mocks!
    >>> mock_client = Mock(api_key='test', timeout=10)
    >>> service = Service(api_client=mock_client)
    >>> main(service)
    <class '__main__.Service'>

See Also:
    - main_before.py: The anti-pattern this code fixes
    - example_02/main.py: Using a DI framework to simplify assembly
    - interfaces.protocols: Protocol definitions for type hints
"""
import os
import sys

# Add project root to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from interfaces import APIClientProtocol


class APIClient:
    """Decoupled API client that receives configuration as parameters.

    This class follows the Dependency Inversion Principle (DIP).
    It doesn't depend on implementation details (like os.getenv),
    only on abstractions (constructor parameters).

    This class satisfies APIClientProtocol without explicit inheritance,
    demonstrating Python's structural subtyping (duck typing).

    Attributes:
        api_key: API key for authentication, injected via constructor.
        timeout: Timeout in seconds for requests, injected via constructor.

    Example:
        >>> client = APIClient(api_key='my-key', timeout=30)
        >>> client.api_key
        'my-key'
        >>> client.timeout
        30

        >>> # Verify it satisfies the protocol
        >>> from interfaces import APIClientProtocol
        >>> isinstance(client, APIClientProtocol)
        True
    """

    def __init__(self, api_key: str, timeout: int) -> None:
        """Initialize client with injected configuration.

        Args:
            api_key: API key for authentication.
            timeout: Timeout in seconds for requests.
        """
        self.api_key = api_key
        self.timeout = timeout


class Service:
    """Decoupled service that receives APIClient as a dependency.

    This class no longer creates its own APIClient instance. Instead,
    it receives an instance through the constructor (Dependency Injection).

    By depending on APIClientProtocol instead of the concrete APIClient,
    this class can work with any implementation that satisfies the protocol,
    including mocks for testing.

    Attributes:
        api_client: API client instance, injected via constructor.
            Must satisfy APIClientProtocol.

    Example:
        >>> from unittest.mock import Mock
        >>> mock_client = Mock(api_key='test', timeout=5)
        >>> service = Service(api_client=mock_client)
        >>> service.api_client.timeout
        5
    """

    def __init__(self, api_client: APIClientProtocol) -> None:
        """Initialize service with injected API client.

        Args:
            api_client: API client for making requests.
                Can be any object satisfying APIClientProtocol.
        """
        self.api_client = api_client


def main(service: Service) -> None:
    """Entry point that receives the service as a parameter.

    This function demonstrates that even the entry point can receive
    its dependencies via injection, making the entire application
    testable and flexible.

    Args:
        service: Service instance to use. Injected by caller.

    Example:
        >>> from unittest.mock import Mock
        >>> mock_service = Mock()
        >>> main(mock_service)  # Works with any mock!
        <class 'unittest.mock.Mock'>
    """
    print(type(service))


# Manual dependency assembly code
# ================================
# This code assembles all dependencies in the correct order.
# It's the ONLY place where concrete implementations are created.
#
# Benefits:
#   - All wiring in one place (easy to find and modify)
#   - Classes are decoupled (easy to test)
#   - Configuration is explicit (no hidden dependencies)
#
# Limitation:
#   - Manual assembly is prone to duplication
#   - Complex dependency graphs become hard to manage
#   - No automatic lifecycle management
#
# Solution: Use a DI container (see example_02/main.py)
if __name__ == '__main__':
    main(service=Service(api_client=APIClient(
        api_key=os.getenv('API_KEY'),
        timeout=int(os.getenv('TIMEOUT'))
    )))
