# app/routes.py
"""HTTP route handlers for the items API."""

from typing import Any

from app import app
from flask import request

items: list[dict[str, Any]] = []

@app.route('/')
def hello() -> str:
    """Return a simple greeting.

    Returns:
        The greeting text.
    """
    return "Hello, Flask!"

@app.route('/items', methods=['GET'])
def get_items() -> dict[str, Any]:
    """Return all stored items.

    Returns:
        A JSON-serializable dict with the list of items under ``items``.
    """
    return {'items': items}

@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id: int) -> dict[str, Any] | tuple[dict[str, Any], int]:
    """Return a single item by its index.

    Args:
        item_id: Zero-based index of the item in the list.

    Returns:
        A dict containing the item, or a tuple of an error dict and the
        HTTP status code 404 if the index is out of range.
    """
    if item_id < len(items):
        return {'item': items[item_id]}
    else:
        return {'error': 'Item not found'}, 404

@app.route('/items', methods=['POST'])
def add_item() -> tuple[dict[str, Any], int]:
    """Add the JSON request body as a new item.

    Returns:
        A tuple of a confirmation message dict and the HTTP status code 201.
    """
    item = request.get_json()
    items.append(item)
    return {'message': 'Item added successfully'}, 201
