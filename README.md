# Dependency Injection

This repository provides a series of practical examples demonstrating how to implement Dependency Injection (DI) in Python applications.

## ¿Qué es Dependency Injection?

Dependency Injection es un patrón de diseño que permite desacoplar las dependencias de una aplicación, facilitando el testing, mantenimiento y escalabilidad del código. En lugar de que los componentes creen sus propias dependencias, estas se "inyectan" desde el exterior.

### Beneficios principales

- **Testabilidad**: Facilita el uso de mocks y stubs en pruebas unitarias
- **Mantenibilidad**: Reduce el acoplamiento entre componentes
- **Flexibilidad**: Permite intercambiar implementaciones fácilmente
- **Reutilización**: Los componentes se vuelven más genéricos y reutilizables

## Requisitos

- Python 3.7 o superior
- pip (gestor de paquetes de Python)

## Instalación

1. Clonar el repositorio:
```bash
git clone <repository-url>
cd python_di_examples
```

2. Instalar las dependencias:
```bash
pip install -r requirements.txt
```

## Variables de entorno

Los ejemplos requieren las siguientes variables de entorno:

```bash
export API_KEY="your-api-key-here"
export TIMEOUT=30
```

## Ejemplos

### [Example 01](example_01/)

Este ejemplo muestra el proceso de desacoplamiento de una aplicación.

**Archivos:**
- [`main_before.py`](example_01/main_before.py): Código con dependencias acopladas
- [`main_di.py`](example_01/main_di.py): Código desacoplado, preparado para DI

En el primer archivo ([`main_before.py`](example_01/main_before.py)) puedes ver cómo la aplicación está estructurada con dependencias acopladas, donde cada clase crea directamente sus dependencias.

El segundo archivo ([`main_di.py`](example_01/main_di.py)) muestra cómo desacoplar estas dependencias del primer ejemplo e incrementar la cohesión, preparando nuestra aplicación para implementar un inyector de dependencias.

**Ejecutar el ejemplo:**
```bash
# Código acoplado
python example_01/main_before.py

# Código desacoplado
python example_01/main_di.py
```

### [Example 02](example_02/)

Este ejemplo muestra cómo implementar un contenedor de inyección de dependencias usando el framework `dependency-injector`.

**Características demostradas:**
- Declaración de un contenedor de DI
- Uso de providers (Singleton vs Factory)
- Configuración desde variables de entorno
- Inyección automática con decoradores
- Override de dependencias para testing

Primero declaramos un contenedor que proporcionará ayuda con el ensamblaje de objetos a ser inyectados. Este ejemplo también muestra cómo sobrescribir dependencias, útil para reemplazar componentes reales con mocks durante las pruebas.

**Ejecutar el ejemplo:**
```bash
python example_02/main.py
```

## Referencias y recursos

### Documentación oficial
- [dependency-injector Documentation](https://python-dependency-injector.ets-labs.org/) - Documentación completa del framework
- [dependency-injector Examples](https://python-dependency-injector.ets-labs.org/examples/index.html) - Más ejemplos de uso

### Conceptos relacionados
- [SOLID Principles](https://en.wikipedia.org/wiki/SOLID) - Principios de diseño orientado a objetos
- [Inversion of Control](https://en.wikipedia.org/wiki/Inversion_of_control) - Patrón de diseño relacionado

### Artículos recomendados
- [Dependency Injection in Python](https://python-dependency-injector.ets-labs.org/introduction/di_in_python.html) - Introducción a DI en Python
- [Why Use Dependency Injection](https://python-dependency-injector.ets-labs.org/introduction/why_use_di.html) - Motivación y casos de uso

## Estructura del proyecto

```
python_di_examples/
├── example_01/          # Desacoplamiento básico
│   ├── main_before.py   # Código acoplado
│   └── main_di.py       # Código desacoplado
├── example_02/          # Dependency Injector framework
│   └── main.py          # Implementación con contenedor
├── requirements.txt     # Dependencias del proyecto
└── README.md           # Este archivo
```

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o pull request para sugerencias o mejoras.

## Licencia

Este proyecto es de código abierto y está disponible para propósitos educativos.
