"""Integration tests that are expected to fail (used to verify failure reporting)."""

from __future__ import annotations

import pytest
import requests
import threading
import time
import os
from collections.abc import Iterator

from app import app


@pytest.fixture(scope="session")
def base_url() -> Iterator[str]:
    """Wait for the Flask server to be reachable and yield its base URL.

    The server is expected to be started externally; this fixture does not
    start it.

    Yields:
        The base URL of the server, e.g. ``http://localhost:5001``.

    Raises:
        RuntimeError: If the server does not respond with HTTP 200 in time.
    """
    # Use a configurable test port to avoid conflicts
    test_port = int(os.environ.get("TEST_PORT", 5001))
    base_url: str = f"http://localhost:{test_port}"
    
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
    """Fail unconditionally, by design.

    Args:
        base_url: Base URL of the running server (unused).
    """
    assert False

