'''
In this example each part of the aplication is coupled, the APIClient
is coupled with the enviroment variables, the Service is coupled with
the APIClient and so on
'''
import os

class APIClient:
    def __init__(self) -> None:
        self.api_key = os.getenv('API_KEY') # <-- dependency
        self.timeout = int(os.getenv('TIMEOUT')) # <-- dependency

class Service:
    def __init__(self) -> None:
        self.api_client = APIClient() # <-- dependency


def main() -> None:
    service = Service() # <-- dependency
    print(type(service))


if __name__ == '__main__':
    main()
