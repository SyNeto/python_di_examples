"""
Example 01 - Código desacoplado preparado para Dependency Injection

Este ejemplo muestra cómo refactorizar el código de main_before.py para
prepararlo para Dependency Injection.

Mejoras implementadas:
1. Las clases reciben sus dependencias como parámetros del constructor
2. No hay creación directa de dependencias dentro de las clases
3. Las dependencias se ensamblan en un solo lugar (main)
4. Fácil de testear con mocks

El único problema que queda es que el código de ensamblaje manual (líneas 40-45)
es propenso a duplicarse y puede volverse complejo en aplicaciones grandes.
Para resolver esto, se usa un contenedor de DI (ver example_02).
"""
import os


class APIClient:
    """
    Cliente API desacoplado que recibe su configuración como parámetros.

    Esta clase ahora sigue el Principio de Inversión de Dependencias (DIP).
    No depende de detalles de implementación, solo de abstracciones (parámetros).

    Args:
        api_key: Clave de API para autenticación
        timeout: Tiempo de espera en segundos para las peticiones
    """

    def __init__(self, api_key: str, timeout: int) -> None:
        self.api_key = api_key
        self.timeout = timeout


class Service:
    """
    Servicio desacoplado que recibe APIClient como dependencia.

    Esta clase ya no crea su propia instancia de APIClient. En su lugar,
    recibe una instancia a través del constructor (Dependency Injection).
    Esto permite inyectar mocks para testing.

    Args:
        api_client: Cliente API para realizar peticiones
    """

    def __init__(self, api_client: APIClient) -> None:
        self.api_client = api_client


def main(service: Service) -> None:
    """
    Función principal que recibe el servicio como parámetro.

    Args:
        service: Instancia del servicio a utilizar
    """
    print(type(service))


# Código de ensamblaje manual de dependencias
# Este código ensambla todas las dependencias en el orden correcto.
# Nota: Este código es propenso a duplicarse y puede volverse complejo.
# Para resolver esto, usa un contenedor de DI (ver example_02/main.py)
if __name__ == '__main__':
    main(service=Service(api_client=APIClient(
        api_key=os.getenv('API_KEY'),
        timeout=int(os.getenv('TIMEOUT'))
    )))
