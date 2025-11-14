"""
Example 01 - Código con dependencias acopladas

Este ejemplo muestra cómo NO estructurar una aplicación. Aquí cada componente
está fuertemente acoplado a sus dependencias:

- APIClient está acoplado a las variables de entorno
- Service está acoplado a la implementación específica de APIClient
- main() está acoplado a la implementación específica de Service

Problemas de este enfoque:
1. Difícil de testear (no puedes inyectar mocks)
2. Difícil de reutilizar componentes en otros contextos
3. Alto acoplamiento entre componentes
4. Baja cohesión del código

Compara este código con main_di.py para ver la diferencia.
"""
import os


class APIClient:
    """
    Cliente API fuertemente acoplado a las variables de entorno.

    Esta clase viola el Principio de Inversión de Dependencias (DIP) porque
    depende directamente de detalles de implementación (os.getenv).
    """

    def __init__(self) -> None:
        self.api_key = os.getenv('API_KEY')  # Dependencia acoplada
        self.timeout = int(os.getenv('TIMEOUT'))  # Dependencia acoplada


class Service:
    """
    Servicio fuertemente acoplado a APIClient.

    Esta clase crea su propia instancia de APIClient, lo que hace imposible
    inyectar una implementación alternativa o un mock para testing.
    """

    def __init__(self) -> None:
        self.api_client = APIClient()  # Dependencia acoplada


def main() -> None:
    """
    Función principal que crea y usa el servicio.

    También está acoplada porque crea directamente una instancia de Service.
    """
    service = Service()  # Dependencia acoplada
    print(type(service))


if __name__ == '__main__':
    main()
