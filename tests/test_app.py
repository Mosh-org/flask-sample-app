# tests/test_app.py

import pytest

from app import app, routes


def test_hello_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.data.decode('utf-8') == "Hello, Flask!"
    assert response.headers['Content-Type'] == 'text/html; charset=utf-8'


def test_add_item_route(client):
    response = client.post('/items', json={"name": "item1"})
    assert response.status_code == 201
    assert response.get_json() == {'message': 'Item added successfully'}


def test_get_item_route(client):
    client.post('/items', json={"name": "item1"})
    response = client.get('/items/0')
    assert response.status_code == 200
    assert response.get_json() == {'item': {'name': 'item1'}}


def test_get_nonexistent_item_route(client):
    response = client.get('/items/1')
    assert response.status_code == 404
    assert response.get_json()['error']['message'] == 'Item not found'


def test_items_state_reset_between_tests():
    assert routes.items == []
