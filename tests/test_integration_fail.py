# tests/test_integration_fail.py
"""Integration tests that include an intentionally failing test."""

import pytest
import requests
import threading
import time
import os
from typing import Iterator
from app import app


@pytest.fixture(scope="session")
def base_url() -> Iterator[str]:
    """Wait for the Flask server to be ready and yield its base URL.

    Yields:
        The base URL of the running server, e.g. ``http://localhost:5001``.

    Raises:
        RuntimeError: If the server does not respond in time.
    """
    # Use a test port to avoid conflicts
    test_port = int(os.environ.get("TEST_PORT", 5001))
    base_url = f"http://localhost:{test_port}"
    
    # Wait for server to be ready
    max_attempts = 4
    for _ in range(max_attempts):
        try:
            response = requests.get(f"{base_url}/", timeout=1)
            if response.status_code == 200:
                break
        except requests.exceptions.RequestException:
            time.sleep(0.1)
    else:
        raise RuntimeError("Server failed to start within expected time")
    
    yield base_url


def test_hello_route(base_url: str) -> None:
    """Test the root endpoint returns correct greeting.

    Args:
        base_url: Base URL of the running server.
    """
    response = requests.get(f"{base_url}/")
    assert response.status_code == 200
    assert response.text == "Hello, Flask!"
    assert response.headers['Content-Type'] == 'text/html; charset=utf-8'


def test_that_always_fails(base_url: str) -> None:
    """Fail unconditionally (intentional, used to verify failure reporting).

    Args:
        base_url: Base URL of the running server.
    """
    assert False

