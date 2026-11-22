"""HTTP route handlers for the in-memory items API."""

from __future__ import annotations

from typing import Any

from flask import request

from app import app

#: In-memory item store; each item is the JSON object posted by a client.
items: list[dict[str, Any]] = []


@app.route('/')
def hello() -> str:
    """Return a greeting for the root endpoint.

    Returns:
        The plain-text greeting ``"Hello, Flask!"``.
    """
    return "Hello, Flask!"


@app.route('/items', methods=['GET'])
def get_items() -> dict[str, list[dict[str, Any]]]:
    """Return every stored item.

    Returns:
        A JSON-serializable dict with all items under the ``"items"`` key.
    """
    return {'items': items}


@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id: int) -> dict[str, dict[str, Any]] | tuple[dict[str, str], int]:
    """Return a single item by its list index.

    Args:
        item_id: Zero-based index of the item in the store.

    Returns:
        ``{'item': <item>}`` when the index is in range; otherwise a tuple of
        an error dict and the HTTP status code 404.
    """
    if item_id < len(items):
        return {'item': items[item_id]}
    else:
        return {'error': 'Item not found'}, 404


@app.route('/items', methods=['POST'])
def add_item() -> tuple[dict[str, str], int]:
    """Append the JSON request body to the item store.

    Returns:
        A tuple of a confirmation message dict and the HTTP status code 201.
    """
    item = request.get_json()
    items.append(item)
    return {'message': 'Item added successfully'}, 201
