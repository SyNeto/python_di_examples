"""
Example 02 - Implementación con Dependency Injector Framework

Este ejemplo muestra cómo usar el framework 'dependency-injector' para
gestionar automáticamente las dependencias de tu aplicación.

Conceptos clave demostrados:

1. Container (Contenedor):
   - Clase que declara y gestiona todas las dependencias
   - Centraliza la configuración del grafo de dependencias
   - Facilita el testing al permitir override de dependencias

2. Providers (Proveedores):
   - Singleton: Crea UNA ÚNICA instancia compartida (ej: conexiones DB, configs)
   - Factory: Crea UNA NUEVA instancia cada vez que se solicita (ej: requests)
   - Configuration: Gestiona configuración desde env vars, archivos, etc.

3. Decorador @inject:
   - Marca funciones que recibirán dependencias automáticamente
   - Permite inyección automática sin pasar parámetros manualmente

4. Override de dependencias:
   - Permite reemplazar dependencias reales con mocks para testing
   - Útil para aislar componentes durante las pruebas

Comparado con example_01/main_di.py, este approach:
- Elimina el código de ensamblaje manual duplicado
- Centraliza la configuración de dependencias
- Facilita el testing con overrides
- Escala mejor en aplicaciones grandes

Documentación: https://python-dependency-injector.ets-labs.org/
"""
import os
from sys import modules
from unittest import mock

from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject


class APIClient:
    """
    Cliente API que requiere configuración externa.

    Esta es la misma clase de example_01, pero ahora será gestionada
    por el contenedor de DI en lugar de ensamblarse manualmente.

    Args:
        api_key: Clave de API para autenticación
        timeout: Tiempo de espera en segundos para las peticiones
    """

    def __init__(self, api_key: str, timeout: int) -> None:
        self.api_key = api_key
        self.timeout = timeout


class Service:
    """
    Servicio que depende de APIClient.

    Args:
        api_client: Cliente API para realizar peticiones
    """

    def __init__(self, api_client: APIClient) -> None:
        self.api_client = api_client


class Container(containers.DeclarativeContainer):
    """
    Contenedor de Dependency Injection.

    Este contenedor declara todas las dependencias de la aplicación y cómo
    deben ser construidas. Define el grafo de dependencias completo.

    Attributes:
        config: Provider de configuración que lee de variables de entorno
        api_client: Provider Singleton que crea UNA instancia compartida de APIClient
        service: Provider Factory que crea NUEVAS instancias de Service cuando se solicita
    """

    # Configuration provider: gestiona configuración desde env vars
    config = providers.Configuration()

    # Singleton provider: UNA ÚNICA instancia compartida
    # Útil para recursos costosos como conexiones a DB, configs, clientes HTTP
    api_client = providers.Singleton(
        APIClient,
        api_key=config.api_key,
        timeout=config.timeout
    )

    # Factory provider: NUEVA instancia cada vez
    # Útil para objetos stateful que no deben compartirse
    service = providers.Factory(
        Service,
        api_client=api_client
    )


@inject
def main(service: Service = Provide[Container.service]) -> None:
    """
    Función principal con inyección automática de dependencias.

    El decorador @inject permite que el contenedor inyecte automáticamente
    la dependencia 'service' sin tener que pasarla manualmente.

    Args:
        service: Servicio inyectado automáticamente por el contenedor.
                 Provide[Container.service] indica QUÉ dependencia inyectar.
    """
    print(type(service))


if __name__ == '__main__':
    # 1. Crear el contenedor
    container = Container()

    # 2. Configurar desde variables de entorno
    container.config.api_key.from_env('API_KEY', required=True)
    container.config.timeout.from_env('TIMEOUT', as_=int, default=5)

    # 3. Wire (conectar) el contenedor con este módulo
    # Esto activa la inyección automática para funciones decoradas con @inject
    container.wire(modules=[__name__])

    # 4. Llamar a main() sin pasar parámetros
    # El decorador @inject inyecta automáticamente la dependencia
    main()

    # 5. Demostración de override para testing
    # Reemplaza api_client real con un Mock para testing
    with container.api_client.override(mock.Mock()):
        main()  # Ahora usa el mock en lugar del APIClient real
