"""
Interfaces module for Dependency Injection examples.

This module exports the Protocol definitions that serve as contracts
for the implementations across all examples.

Example:
    >>> from interfaces import APIClientProtocol, ServiceProtocol
    >>>
    >>> def process_request(client: APIClientProtocol) -> None:
    ...     print(f"Using client with timeout: {client.timeout}")
"""
from interfaces.protocols import APIClientProtocol, ServiceProtocol

__all__ = ["APIClientProtocol", "ServiceProtocol"]
