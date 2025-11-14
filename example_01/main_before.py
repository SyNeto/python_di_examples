"""
Example 01 - Code with tightly coupled dependencies

This example shows how NOT to structure an application. Here each component
is tightly coupled to its dependencies:

- APIClient is coupled to environment variables
- Service is coupled to the specific APIClient implementation
- main() is coupled to the specific Service implementation

Problems with this approach:
1. Difficult to test (you can't inject mocks)
2. Difficult to reuse components in other contexts
3. High coupling between components
4. Low code cohesion

Compare this code with main_di.py to see the difference.
"""
import os


class APIClient:
    """
    API client tightly coupled to environment variables.

    This class violates the Dependency Inversion Principle (DIP) because
    it depends directly on implementation details (os.getenv).
    """

    def __init__(self) -> None:
        self.api_key = os.getenv('API_KEY')  # Coupled dependency
        self.timeout = int(os.getenv('TIMEOUT'))  # Coupled dependency


class Service:
    """
    Service tightly coupled to APIClient.

    This class creates its own instance of APIClient, making it impossible
    to inject an alternative implementation or a mock for testing.
    """

    def __init__(self) -> None:
        self.api_client = APIClient()  # Coupled dependency


def main() -> None:
    """
    Main function that creates and uses the service.

    It's also coupled because it directly creates a Service instance.
    """
    service = Service()  # Coupled dependency
    print(type(service))


if __name__ == '__main__':
    main()
