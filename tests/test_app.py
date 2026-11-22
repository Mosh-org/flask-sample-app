# tests/test_app.py
"""Unit tests for the Flask application routes using the test client."""

import unittest
from typing import Any
from app import app

class TestAppRoutes(unittest.TestCase):
    """Tests for the HTTP routes exposed by the app."""

    app: Any

    def setUp(self) -> None:
        """Create a test client for each test."""
        self.app = app.test_client()
        self.app.testing = True

    def test_hello_route(self) -> None:
        """Verify GET / returns the greeting."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), "Hello, Flask!")

    def test_add_item_route(self) -> None:
        """Verify POST /items stores an item and returns 201."""
        response = self.app.post('/items', json={"name": "item1"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json(), {'message': 'Item added successfully'})

    def test_get_item_route(self) -> None:
        """Verify GET /items/0 returns the previously added item."""
        response = self.app.get('/items/0')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'item': {'name': 'item1'}})

    def test_get_nonexistent_item_route(self) -> None:
        """Verify GET /items/1 returns 404 when the item is missing."""
        response = self.app.get('/items/1')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {'error': 'Item not found'})

if __name__ == '__main__':
    unittest.main()
