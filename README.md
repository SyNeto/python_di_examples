# Dependency Injection in Python

This repository provides practical examples demonstrating how to implement Dependency Injection (DI) in Python applications, progressing from basic concepts to framework-based solutions.

> **Note**: This project was developed with assistance from [Claude Code](https://claude.ai/claude-code). The original concepts and documentation focus came from a human developer, while Claude Code helped improve documentation consistency, add Protocol interfaces, and create comprehensive test examples. We believe in transparency about AI-assisted development.

## What is Dependency Injection?

Dependency Injection is a design pattern that decouples components from their dependencies. Instead of components creating their own dependencies internally, they receive them from the outside (injection).

### The Problem (Without DI)

```python
class Service:
    def __init__(self):
        self.client = APIClient()  # Tightly coupled!
```

Problems:
- Cannot test without real APIClient
- Cannot swap implementations
- Hidden dependencies

### The Solution (With DI)

```python
class Service:
    def __init__(self, client: APIClientProtocol):  # Injected!
        self.client = client
```

Benefits:
- **Testability**: Inject mocks for testing
- **Flexibility**: Swap implementations easily
- **Clarity**: Dependencies are explicit

## Key Benefits

| Benefit | Description |
|---------|-------------|
| **Testability** | Inject mocks instead of real dependencies |
| **Maintainability** | Reduced coupling between components |
| **Flexibility** | Easy to swap implementations |
| **Reusability** | Components work in different contexts |

## Documentation Standards

This project uses a combination of documentation approaches for maximum clarity:

| Approach | Purpose | Example |
|----------|---------|---------|
| **Type Hints** | IDE autocompletion, static analysis | `def get_user(id: int) -> User` |
| **Google Docstrings** | Human-readable documentation | Args, Returns, Example sections |
| **Protocols (PEP 544)** | Interface definitions without inheritance | `class APIClientProtocol(Protocol)` |

## Requirements

- Python 3.8 or higher (Protocol support)
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd python_di_examples
```

2. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
# Production only
pip install -r requirements.txt

# Development (includes pytest)
pip install -r requirements-dev.txt
```

## Environment Variables

Copy the example file and configure:

```bash
cp .env.example .env
```

Required variables:
```bash
API_KEY=your-api-key-here
TIMEOUT=30
```

Or export directly:
```bash
export API_KEY="your-api-key"
export TIMEOUT=30
```

## Examples

### [Example 01](example_01/) - Fundamentals

Demonstrates the journey from tightly coupled code to properly decoupled code.

| File | Description |
|------|-------------|
| [`main_before.py`](example_01/main_before.py) | Anti-pattern: tightly coupled dependencies |
| [`main_di.py`](example_01/main_di.py) | Solution: manual dependency injection |

**Run:**
```bash
python example_01/main_before.py  # See the problem
python example_01/main_di.py      # See the solution
```

**Key learning**: Understand WHY DI matters before using frameworks.

---

### [Example 02](example_02/) - Framework DI

Introduces the `dependency-injector` framework to solve manual assembly limitations.

**Features demonstrated:**
- Container pattern for dependency management
- Providers: Singleton vs Factory
- Configuration from environment variables
- Automatic injection with `@inject` decorator
- Override for testing

**Run:**
```bash
python example_02/main.py
```

**Key learning**: Frameworks reduce boilerplate and add lifecycle management.

---

### [Example 03](example_03/) - Testing with DI

Shows the PRIMARY benefit of DI: testability with mocks.

| File | Description |
|------|-------------|
| [`main.py`](example_03/main.py) | Testable implementation with UserService |
| [`test_main.py`](example_03/test_main.py) | pytest tests demonstrating mock injection |

**Run:**
```bash
python example_03/main.py                    # Run the example
pytest example_03/test_main.py -v            # Run tests
```

**Key learning**: DI enables isolated, fast, reliable tests.

---

### [Interfaces](interfaces/) - Protocol Definitions

Shared Protocol definitions used across all examples.

```python
from interfaces import APIClientProtocol, ServiceProtocol
```

**Key learning**: Protocols enable duck typing with type safety.

## Project Structure

```
python_di_examples/
├── interfaces/              # Protocol definitions (contracts)
│   ├── __init__.py
│   └── protocols.py         # APIClientProtocol, ServiceProtocol
├── example_01/              # Fundamentals: coupling vs decoupling
│   ├── __init__.py
│   ├── main_before.py       # Anti-pattern (tightly coupled)
│   └── main_di.py           # Solution (manual DI)
├── example_02/              # Framework: dependency-injector
│   ├── __init__.py
│   └── main.py              # Container, providers, wiring
├── example_03/              # Testing: mocks with DI
│   ├── __init__.py
│   ├── main.py              # Testable implementation
│   └── test_main.py         # pytest examples
├── .env.example             # Environment template
├── .python-version          # Python 3.8+
├── requirements.txt         # Production dependencies
├── requirements-dev.txt     # Development dependencies
└── README.md                # This file
```

## Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific example tests
pytest example_03/test_main.py -v

# Run with coverage (if installed)
pytest --cov=. --cov-report=html
```

## References and Resources

### Official Documentation
- [dependency-injector Documentation](https://python-dependency-injector.ets-labs.org/)
- [dependency-injector Examples](https://python-dependency-injector.ets-labs.org/examples/index.html)
- [PEP 544 - Protocols](https://peps.python.org/pep-0544/)

### Related Concepts
- [SOLID Principles](https://en.wikipedia.org/wiki/SOLID)
- [Inversion of Control](https://en.wikipedia.org/wiki/Inversion_of_control)
- [Dependency Inversion Principle](https://en.wikipedia.org/wiki/Dependency_inversion_principle)

### Recommended Articles
- [Dependency Injection in Python](https://python-dependency-injector.ets-labs.org/introduction/di_in_python.html)
- [Why Use Dependency Injection](https://python-dependency-injector.ets-labs.org/introduction/why_use_di.html)

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Follow the documentation standards (Type Hints + Google Docstrings + Protocols)
4. Add tests for new functionality
5. Submit a pull request

## License

This project is open source and available for educational purposes.
