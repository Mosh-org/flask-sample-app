"""HTTP routes for the in-memory items REST API."""

from typing import Any

from flask import request

from app import app

items: list[Any] = []


@app.route('/')
def hello() -> str:
    """Return a simple greeting.

    Returns:
        The greeting text.
    """
    return "Hello, Flask!"


@app.route('/items', methods=['GET'])
def get_items() -> dict[str, list[Any]]:
    """Return all stored items.

    Returns:
        A JSON-serializable mapping with the list of items under ``items``.
    """
    return {'items': items}


@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id: int) -> dict[str, Any] | tuple[dict[str, str], int]:
    """Return a single item by its index.

    Args:
        item_id: Index of the item in the list. Negative values are not
            rejected by the bounds check and index from the end of the list.

    Returns:
        A mapping with the item, or an error mapping and HTTP 404 if the
        index is out of range.
    """
    if item_id < len(items):
        return {'item': items[item_id]}
    else:
        return {'error': 'Item not found'}, 404


@app.route('/items', methods=['POST'])
def add_item() -> tuple[dict[str, str], int]:
    """Append the JSON request body to the item list.

    Returns:
        A confirmation message and HTTP 201.
    """
    item = request.get_json()
    items.append(item)
    return {'message': 'Item added successfully'}, 201
