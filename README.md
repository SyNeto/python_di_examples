# Dependency Injection

This repository provides a series of practical examples demonstrating how to implement Dependency Injection (DI) in Python applications.

## What is Dependency Injection?

Dependency Injection is a design pattern that allows decoupling dependencies in an application, facilitating testing, maintenance, and code scalability. Instead of components creating their own dependencies, they are "injected" from outside.

### Key Benefits

- **Testability**: Facilitates the use of mocks and stubs in unit tests
- **Maintainability**: Reduces coupling between components
- **Flexibility**: Allows easy swapping of implementations
- **Reusability**: Components become more generic and reusable

## Requirements

- Python 3.7 or higher
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd python_di_examples
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Environment Variables

The examples require the following environment variables:

```bash
export API_KEY="your-api-key-here"
export TIMEOUT=30
```

## Examples

### [Example 01](example_01/)

This example demonstrates the process of decoupling an application.

**Files:**
- [`main_before.py`](example_01/main_before.py): Code with tightly coupled dependencies
- [`main_di.py`](example_01/main_di.py): Decoupled code, prepared for DI

In the first file ([`main_before.py`](example_01/main_before.py)) you can see how the application is structured with tightly coupled dependencies, where each class directly creates its own dependencies.

The second file ([`main_di.py`](example_01/main_di.py)) shows how to decouple these dependencies from the first example and increase cohesion, preparing our application to implement a dependency injector.

**Run the example:**
```bash
# Tightly coupled code
python example_01/main_before.py

# Decoupled code
python example_01/main_di.py
```

### [Example 02](example_02/)

This example demonstrates how to implement a dependency injection container using the `dependency-injector` framework.

**Features demonstrated:**
- Declaration of a DI container
- Use of providers (Singleton vs Factory)
- Configuration from environment variables
- Automatic injection with decorators
- Dependency override for testing

First we declare a container that will provide help with the assembly of objects to be injected. This example also shows how to override dependencies, useful for replacing real components with mocks during testing.

**Run the example:**
```bash
python example_02/main.py
```

## References and Resources

### Official Documentation
- [dependency-injector Documentation](https://python-dependency-injector.ets-labs.org/) - Complete framework documentation
- [dependency-injector Examples](https://python-dependency-injector.ets-labs.org/examples/index.html) - More usage examples

### Related Concepts
- [SOLID Principles](https://en.wikipedia.org/wiki/SOLID) - Object-oriented design principles
- [Inversion of Control](https://en.wikipedia.org/wiki/Inversion_of_control) - Related design pattern

### Recommended Articles
- [Dependency Injection in Python](https://python-dependency-injector.ets-labs.org/introduction/di_in_python.html) - Introduction to DI in Python
- [Why Use Dependency Injection](https://python-dependency-injector.ets-labs.org/introduction/why_use_di.html) - Motivation and use cases

## Project Structure

```
python_di_examples/
├── example_01/          # Basic decoupling
│   ├── main_before.py   # Tightly coupled code
│   └── main_di.py       # Decoupled code
├── example_02/          # Dependency Injector framework
│   └── main.py          # Implementation with container
├── requirements.txt     # Project dependencies
└── README.md           # This file
```

## Contributing

Contributions are welcome. Please open an issue or pull request for suggestions or improvements.

## License

This project is open source and available for educational purposes.
