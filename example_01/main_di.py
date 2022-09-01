# this example code shows how to prepare the code on main_before.py
# and provide a way to to inject the dependencies.
import os

class APIClient:
    def __init__(self, api_key: str, timeout: int) -> None:
        self.api_key = api_key
        self.timeout = timeout


class Service:
    def __init__(self, api_client: APIClient) -> None:
        self.api_client = api_client


def main(service: Service) -> None:
    print(type(service))

# this assembly code is prone to be duplicated and it will couple the
# application structure, to solve this, use a dependency injector.
if __name__ == '__main__':
    main(service=Service(api_client=APIClient(
       api_key=os.getenv('API_KEY'),
       timeout=int(os.getenv('TIMEOUT')) 
    )))