"""
Example 01 - Code with tightly coupled dependencies (Anti-pattern).

This example demonstrates how NOT to structure an application. Each component
is tightly coupled to its dependencies, violating the Dependency Inversion
Principle (DIP) from SOLID.

Problems illustrated:
    1. **Hard to test**: Cannot inject mocks without modifying source code.
    2. **Hard to reuse**: Components only work with specific implementations.
    3. **High coupling**: Changes in one component cascade to others.
    4. **Hidden dependencies**: Dependencies are buried inside constructors.

Learning objective:
    Recognize these patterns in your own code as signals that refactoring
    is needed. Compare with main_di.py to see the solution.

Example:
    >>> # This code requires real environment variables to run
    >>> # You cannot easily test it with fake values
    >>> import os
    >>> os.environ['API_KEY'] = 'test'
    >>> os.environ['TIMEOUT'] = '30'
    >>> main()
    <class '__main__.Service'>

Warning:
    This is an ANTI-PATTERN shown for educational purposes.
    Do NOT copy this structure in production code.

See Also:
    - main_di.py: The refactored version with proper DI
    - example_02/main.py: Using a DI framework
"""
import os


class APIClient:
    """API client tightly coupled to environment variables.

    This class violates the Dependency Inversion Principle (DIP) because
    it depends directly on implementation details (os.getenv) rather than
    receiving its configuration as parameters.

    Problems:
        - Cannot test without setting real environment variables.
        - Cannot reuse with different configurations.
        - Hidden dependencies make the class harder to understand.

    Attributes:
        api_key: API key read directly from environment.
        timeout: Timeout read directly from environment.

    Raises:
        TypeError: If TIMEOUT environment variable is not set or not numeric.
    """

    def __init__(self) -> None:
        """Initialize client by reading from environment variables.

        Warning:
            This constructor has HIDDEN dependencies on environment variables.
            This is the anti-pattern we want to avoid.
        """
        self.api_key = os.getenv('API_KEY')  # Coupled dependency
        self.timeout = int(os.getenv('TIMEOUT'))  # Coupled dependency


class Service:
    """Service tightly coupled to APIClient implementation.

    This class creates its own instance of APIClient internally,
    making it impossible to inject an alternative implementation
    or a mock for testing.

    Problems:
        - Cannot test Service without also testing APIClient.
        - Cannot swap APIClient for a different implementation.
        - Service "knows too much" about how to create its dependencies.

    Attributes:
        api_client: Internally created APIClient instance.
    """

    def __init__(self) -> None:
        """Initialize service by creating its own APIClient.

        Warning:
            Creating dependencies inside the constructor is an anti-pattern.
            Dependencies should be INJECTED, not created.
        """
        self.api_client = APIClient()  # Coupled dependency


def main() -> None:
    """Entry point that creates and uses the service.

    This function is also coupled because it directly creates a Service
    instance. In a properly structured application, the Service would
    be injected as a parameter.

    Note:
        The entire call chain (main -> Service -> APIClient -> os.getenv)
        is tightly coupled. Any change requires modifying multiple files.
    """
    service = Service()  # Coupled dependency
    print(type(service))


if __name__ == '__main__':
    main()
