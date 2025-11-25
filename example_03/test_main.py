"""
Example 03 - Tests demonstrating Dependency Injection benefits.

This module shows the PRIMARY benefit of DI: testability.

Without DI, testing UserService would require:
    - Real API calls (slow, flaky, needs network)
    - Environment setup (API keys, servers)
    - Complex mocking with patches

With DI, testing is simple:
    - Create a mock with the expected interface
    - Inject it into the class under test
    - Assert behavior without any real I/O

Test patterns demonstrated:
    1. **Mock injection**: Pass mocks via constructor
    2. **Behavior verification**: Check that methods were called correctly
    3. **Response control**: Define exactly what the mock returns
    4. **Edge cases**: Test error conditions easily
    5. **Isolation**: Each test is independent

Run tests:
    pytest example_03/test_main.py -v

Example output:
    test_get_user_returns_user_when_found PASSED
    test_get_user_returns_none_when_not_found PASSED
    test_is_user_active_returns_true_for_active_user PASSED
    ...
"""
import pytest
from unittest.mock import Mock, MagicMock

from example_03.main import User, UserService, HTTPAPIClient


class TestUserService:
    """Tests for UserService demonstrating DI benefits.

    Each test creates its own mock, showing how DI enables:
        - Complete isolation between tests
        - Control over dependency behavior
        - No need for real external services

    Fixture pattern:
        We use pytest fixtures to reduce boilerplate.
        The mock_client fixture creates a fresh mock for each test.
    """

    @pytest.fixture
    def mock_client(self) -> Mock:
        """Create a mock API client for testing.

        Returns:
            Mock object configured with api_key and timeout attributes.
            The get() method is a MagicMock ready to be configured.

        Note:
            Each test gets a FRESH mock, ensuring isolation.
        """
        mock = Mock()
        mock.api_key = 'test-key'
        mock.timeout = 10
        return mock

    @pytest.fixture
    def service(self, mock_client: Mock) -> UserService:
        """Create a UserService with mock client.

        Args:
            mock_client: The mock API client fixture.

        Returns:
            UserService instance with mock injected.
        """
        return UserService(api_client=mock_client)

    # =========================================================================
    # Tests for get_user()
    # =========================================================================

    def test_get_user_returns_user_when_found(
        self,
        service: UserService,
        mock_client: Mock
    ) -> None:
        """Test that get_user returns a User when API returns data.

        This test demonstrates:
            1. Configure mock to return specific data
            2. Call the method under test
            3. Assert the result matches expectations
            4. Verify the mock was called correctly
        """
        # Arrange: Configure mock response
        mock_client.get.return_value = {
            'id': 1,
            'name': 'Alice',
            'email': 'alice@example.com',
            'active': True
        }

        # Act: Call the method under test
        user = service.get_user(1)

        # Assert: Check the result
        assert user is not None
        assert user.id == 1
        assert user.name == 'Alice'
        assert user.email == 'alice@example.com'
        assert user.active is True

        # Verify: Check the mock was called correctly
        mock_client.get.assert_called_once_with('/users/1')

    def test_get_user_returns_none_when_not_found(
        self,
        service: UserService,
        mock_client: Mock
    ) -> None:
        """Test that get_user returns None when API returns empty response.

        This demonstrates testing edge cases with controlled mock responses.
        """
        # Arrange: Configure mock to return empty (user not found)
        mock_client.get.return_value = {}

        # Act
        user = service.get_user(999)

        # Assert
        assert user is None
        mock_client.get.assert_called_once_with('/users/999')

    def test_get_user_handles_inactive_user(
        self,
        service: UserService,
        mock_client: Mock
    ) -> None:
        """Test that get_user correctly handles inactive users."""
        # Arrange
        mock_client.get.return_value = {
            'id': 2,
            'name': 'Bob',
            'email': 'bob@example.com',
            'active': False
        }

        # Act
        user = service.get_user(2)

        # Assert
        assert user is not None
        assert user.active is False

    def test_get_user_defaults_active_to_true(
        self,
        service: UserService,
        mock_client: Mock
    ) -> None:
        """Test that missing 'active' field defaults to True.

        This tests defensive coding in the service.
        """
        # Arrange: Response missing 'active' field
        mock_client.get.return_value = {
            'id': 3,
            'name': 'Charlie',
            'email': 'charlie@example.com'
            # Note: 'active' is missing
        }

        # Act
        user = service.get_user(3)

        # Assert: Should default to True
        assert user is not None
        assert user.active is True

    # =========================================================================
    # Tests for is_user_active()
    # =========================================================================

    def test_is_user_active_returns_true_for_active_user(
        self,
        service: UserService,
        mock_client: Mock
    ) -> None:
        """Test is_user_active returns True for active users."""
        # Arrange
        mock_client.get.return_value = {
            'id': 1,
            'name': 'Active User',
            'email': 'active@example.com',
            'active': True
        }

        # Act & Assert
        assert service.is_user_active(1) is True

    def test_is_user_active_returns_false_for_inactive_user(
        self,
        service: UserService,
        mock_client: Mock
    ) -> None:
        """Test is_user_active returns False for inactive users."""
        # Arrange
        mock_client.get.return_value = {
            'id': 1,
            'name': 'Inactive User',
            'email': 'inactive@example.com',
            'active': False
        }

        # Act & Assert
        assert service.is_user_active(1) is False

    def test_is_user_active_returns_false_for_nonexistent_user(
        self,
        service: UserService,
        mock_client: Mock
    ) -> None:
        """Test is_user_active returns False when user doesn't exist."""
        # Arrange
        mock_client.get.return_value = {}

        # Act & Assert
        assert service.is_user_active(999) is False


class TestHTTPAPIClient:
    """Tests for HTTPAPIClient (the real implementation).

    These tests verify the simulated behavior works correctly.
    In a real application, you might skip unit tests for HTTP clients
    and test them via integration tests instead.
    """

    def test_client_stores_configuration(self) -> None:
        """Test that client stores api_key and timeout."""
        client = HTTPAPIClient(api_key='test-key', timeout=30)

        assert client.api_key == 'test-key'
        assert client.timeout == 30

    def test_get_returns_simulated_user(self) -> None:
        """Test the simulated GET response for users."""
        client = HTTPAPIClient(api_key='key', timeout=10)

        response = client.get('/users/42')

        assert response['id'] == 42
        assert response['name'] == 'User 42'
        assert response['email'] == 'user42@example.com'


class TestUser:
    """Tests for User dataclass."""

    def test_user_creation(self) -> None:
        """Test creating a User with all fields."""
        user = User(id=1, name='Test', email='test@example.com', active=True)

        assert user.id == 1
        assert user.name == 'Test'
        assert user.email == 'test@example.com'
        assert user.active is True

    def test_user_active_defaults_to_true(self) -> None:
        """Test that active defaults to True if not specified."""
        user = User(id=1, name='Test', email='test@example.com')

        assert user.active is True


# =============================================================================
# Integration-style test showing full flow
# =============================================================================

class TestIntegration:
    """Integration test showing how components work together.

    This test uses the real HTTPAPIClient (with simulated responses)
    to verify the full flow works correctly.
    """

    def test_full_flow_with_real_client(self) -> None:
        """Test UserService with real (simulated) HTTPAPIClient.

        This is closer to an integration test, verifying that
        all components work together correctly.
        """
        # Arrange: Use real client (with simulated responses)
        client = HTTPAPIClient(api_key='integration-key', timeout=30)
        service = UserService(api_client=client)

        # Act
        user = service.get_user(100)

        # Assert
        assert user is not None
        assert user.id == 100
        assert user.name == 'User 100'
        assert service.is_user_active(100) is True
