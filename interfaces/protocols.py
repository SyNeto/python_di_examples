"""
Protocol definitions for Dependency Injection examples.

This module defines contracts (interfaces) using Python's Protocol class
from typing module. Protocols enable structural subtyping (duck typing)
without requiring explicit inheritance.

Why Protocols over ABC (Abstract Base Classes)?
    - No inheritance required: any class with matching structure satisfies the protocol
    - More Pythonic: embraces duck typing philosophy
    - Better for DI: implementations don't need to know about the interface
    - Easier testing: mocks automatically satisfy protocols if they have the right attributes

References:
    - PEP 544: https://peps.python.org/pep-0544/
    - typing.Protocol: https://docs.python.org/3/library/typing.html#typing.Protocol
"""
from typing import Protocol, runtime_checkable


@runtime_checkable
class APIClientProtocol(Protocol):
    """Contract for API client implementations.

    This protocol defines the expected structure for any API client.
    Any class with matching attributes satisfies this protocol,
    enabling loose coupling and easy testing with mocks.

    The @runtime_checkable decorator allows using isinstance() checks,
    useful for validation and debugging.

    Attributes:
        api_key: Authentication key for API requests.
        timeout: Request timeout in seconds.

    Example:
        >>> class ProductionClient:
        ...     def __init__(self, api_key: str, timeout: int) -> None:
        ...         self.api_key = api_key
        ...         self.timeout = timeout
        ...
        >>> client = ProductionClient("secret", 30)
        >>> isinstance(client, APIClientProtocol)
        True

        >>> # Mocks also satisfy the protocol
        >>> from unittest.mock import Mock
        >>> mock_client = Mock(api_key="test", timeout=5)
        >>> isinstance(mock_client, APIClientProtocol)
        True

    Note:
        Protocols define WHAT an object must have, not HOW it should be created.
        This is the key difference from abstract classes.
    """

    api_key: str
    timeout: int


@runtime_checkable
class ServiceProtocol(Protocol):
    """Contract for service implementations.

    Defines the expected structure for services that depend on an API client.
    This protocol demonstrates how DI works at multiple levels:
    the Service depends on APIClientProtocol, not a concrete implementation.

    Attributes:
        api_client: The API client instance used for making requests.
            Must satisfy APIClientProtocol.

    Example:
        >>> class MyService:
        ...     def __init__(self, api_client: APIClientProtocol) -> None:
        ...         self.api_client = api_client
        ...
        >>> # With a real client
        >>> real_client = ProductionClient("key", 30)
        >>> service = MyService(real_client)
        >>> isinstance(service, ServiceProtocol)
        True

        >>> # With a mock (for testing)
        >>> mock_client = Mock(api_key="test", timeout=5)
        >>> test_service = MyService(mock_client)
        >>> isinstance(test_service, ServiceProtocol)
        True

    Note:
        The api_client attribute is typed as APIClientProtocol, showing
        how protocols compose together to define complex contracts.
    """

    api_client: APIClientProtocol
