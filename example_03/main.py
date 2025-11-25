"""
Example 03 - Testable implementation with Dependency Injection.

This example demonstrates a more realistic implementation that shows
WHY dependency injection matters: testability.

The UserService depends on APIClientProtocol. Because we use DI:
    - In production: inject a real HTTP client
    - In tests: inject a mock that returns controlled responses

Key patterns demonstrated:
    1. **Protocol-based dependencies**: Depend on interfaces, not implementations.
    2. **Constructor injection**: All dependencies passed via __init__.
    3. **Testable design**: No hidden dependencies, no global state.
    4. **Separation of concerns**: Business logic separate from I/O.

Example:
    >>> # Production usage
    >>> client = HTTPAPIClient(api_key='real-key', timeout=30)
    >>> service = UserService(api_client=client)
    >>> user = service.get_user(123)  # Makes real HTTP call

    >>> # Test usage
    >>> from unittest.mock import Mock
    >>> mock_client = Mock()
    >>> mock_client.get.return_value = {'id': 1, 'name': 'Test'}
    >>> service = UserService(api_client=mock_client)
    >>> user = service.get_user(1)  # No HTTP call, uses mock!

See Also:
    - test_main.py: Tests demonstrating these patterns
    - interfaces.protocols: Protocol definitions
"""
import os
import sys
from dataclasses import dataclass
from typing import Optional

# Add project root to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from interfaces import APIClientProtocol


@dataclass
class User:
    """Data class representing a user.

    Using dataclass for clean, immutable data structures.
    This is the domain model, separate from API responses.

    Attributes:
        id: Unique user identifier.
        name: User's display name.
        email: User's email address.
        active: Whether the user account is active.

    Example:
        >>> user = User(id=1, name='Alice', email='alice@example.com')
        >>> user.active
        True
    """

    id: int
    name: str
    email: str
    active: bool = True


class HTTPAPIClient:
    """Production API client that makes real HTTP requests.

    This class satisfies APIClientProtocol and would make actual
    HTTP calls in a real application.

    For this example, we simulate responses to keep it simple.
    In production, you would use requests, httpx, or aiohttp.

    Attributes:
        api_key: API key for authentication.
        timeout: Request timeout in seconds.

    Example:
        >>> client = HTTPAPIClient(api_key='secret', timeout=30)
        >>> response = client.get('/users/1')
        >>> response['id']
        1
    """

    def __init__(self, api_key: str, timeout: int) -> None:
        """Initialize HTTP client with configuration.

        Args:
            api_key: API key for authentication.
            timeout: Request timeout in seconds.
        """
        self.api_key = api_key
        self.timeout = timeout

    def get(self, endpoint: str) -> dict:
        """Make a GET request to the API.

        Args:
            endpoint: API endpoint path (e.g., '/users/1').

        Returns:
            Dictionary containing the API response.

        Note:
            This is a simulation. Real implementation would use
            requests.get() or similar.
        """
        # Simulated response for demonstration
        # In production: return requests.get(f"{base_url}{endpoint}").json()
        if endpoint.startswith('/users/'):
            user_id = int(endpoint.split('/')[-1])
            return {
                'id': user_id,
                'name': f'User {user_id}',
                'email': f'user{user_id}@example.com',
                'active': True
            }
        return {}


class UserService:
    """Service for user operations with injected dependencies.

    This is the class we want to test. It depends on APIClientProtocol,
    not a concrete implementation. This allows us to:
        - Inject a real client in production
        - Inject a mock in tests

    The service contains business logic that transforms API responses
    into domain objects (User).

    Attributes:
        api_client: API client for making requests. Must have a get() method.

    Example:
        >>> # With real client
        >>> client = HTTPAPIClient(api_key='key', timeout=30)
        >>> service = UserService(api_client=client)
        >>> user = service.get_user(1)
        >>> user.name
        'User 1'

        >>> # With mock (for testing)
        >>> from unittest.mock import Mock
        >>> mock = Mock()
        >>> mock.get.return_value = {'id': 99, 'name': 'Mock User', 'email': 'mock@test.com', 'active': True}
        >>> service = UserService(api_client=mock)
        >>> user = service.get_user(99)
        >>> user.name
        'Mock User'
    """

    def __init__(self, api_client: APIClientProtocol) -> None:
        """Initialize service with injected API client.

        Args:
            api_client: API client for making requests.
                Can be any object with api_key, timeout attributes
                and a get() method.
        """
        self.api_client = api_client

    def get_user(self, user_id: int) -> Optional[User]:
        """Fetch a user by ID.

        Makes an API call and transforms the response into a User object.
        Returns None if the user is not found.

        Args:
            user_id: The unique identifier of the user.

        Returns:
            User object if found, None otherwise.

        Example:
            >>> service = UserService(api_client=client)
            >>> user = service.get_user(123)
            >>> if user:
            ...     print(f"Found: {user.name}")
        """
        response = self.api_client.get(f'/users/{user_id}')

        if not response:
            return None

        return User(
            id=response['id'],
            name=response['name'],
            email=response['email'],
            active=response.get('active', True)
        )

    def is_user_active(self, user_id: int) -> bool:
        """Check if a user is active.

        Convenience method that fetches the user and checks their status.

        Args:
            user_id: The unique identifier of the user.

        Returns:
            True if user exists and is active, False otherwise.

        Example:
            >>> service = UserService(api_client=client)
            >>> service.is_user_active(123)
            True
        """
        user = self.get_user(user_id)
        return user is not None and user.active


def main() -> None:
    """Demonstrate the service with a real client.

    This shows how the components work together in production-like usage.
    """
    # Create dependencies
    api_key = os.getenv('API_KEY', 'demo-key')
    timeout = int(os.getenv('TIMEOUT', '30'))

    client = HTTPAPIClient(api_key=api_key, timeout=timeout)
    service = UserService(api_client=client)

    # Use the service
    user = service.get_user(42)
    if user:
        print(f"Found user: {user.name} ({user.email})")
        print(f"Active: {user.active}")
    else:
        print("User not found")


if __name__ == '__main__':
    main()
