"""
Example 01 - Decoupled code prepared for Dependency Injection

This example shows how to refactor the code from main_before.py to
prepare it for Dependency Injection.

Improvements implemented:
1. Classes receive their dependencies as constructor parameters
2. No direct creation of dependencies within classes
3. Dependencies are assembled in a single place (main)
4. Easy to test with mocks

The only remaining problem is that the manual assembly code (lines 40-45)
is prone to duplication and can become complex in large applications.
To solve this, use a DI container (see example_02).
"""
import os


class APIClient:
    """
    Decoupled API client that receives its configuration as parameters.

    This class now follows the Dependency Inversion Principle (DIP).
    It doesn't depend on implementation details, only on abstractions (parameters).

    Args:
        api_key: API key for authentication
        timeout: Timeout in seconds for requests
    """

    def __init__(self, api_key: str, timeout: int) -> None:
        self.api_key = api_key
        self.timeout = timeout


class Service:
    """
    Decoupled service that receives APIClient as a dependency.

    This class no longer creates its own APIClient instance. Instead,
    it receives an instance through the constructor (Dependency Injection).
    This allows injecting mocks for testing.

    Args:
        api_client: API client for making requests
    """

    def __init__(self, api_client: APIClient) -> None:
        self.api_client = api_client


def main(service: Service) -> None:
    """
    Main function that receives the service as a parameter.

    Args:
        service: Service instance to use
    """
    print(type(service))


# Manual dependency assembly code
# This code assembles all dependencies in the correct order.
# Note: This code is prone to duplication and can become complex.
# To solve this, use a DI container (see example_02/main.py)
if __name__ == '__main__':
    main(service=Service(api_client=APIClient(
        api_key=os.getenv('API_KEY'),
        timeout=int(os.getenv('TIMEOUT'))
    )))
