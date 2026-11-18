# app/routes.py
"""HTTP routes for the sample Flask app.

Defines a greeting route and a small in-memory item store exposed through
``GET /items``, ``GET /items/<item_id>`` and ``POST /items``. Items live in the
module-level ``items`` list and are lost when the process exits.
"""

from typing import Any

from app import app
from flask import request

items: list[Any] = []

@app.route('/')
def hello() -> str:
    """Return a greeting.

    Returns:
        The plain-text string ``"Hello, Flask!"``.
    """
    return "Hello, Flask!"

@app.route('/items', methods=['GET'])
def get_items() -> dict[str, Any]:
    """List all stored items.

    Returns:
        A dict with a single ``items`` key holding the list of stored items.
    """
    return {'items': items}

@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id: int) -> dict[str, Any] | tuple[dict[str, Any], int]:
    """Fetch a single item by its position in the store.

    Negative values of ``item_id`` are not rejected: the route's ``int``
    converter only matches non-negative digits in practice, but the function
    itself performs only an upper-bound check (``item_id < len(items)``), so a
    negative index passed directly would be treated as in range and use
    Python's negative list indexing.

    Args:
        item_id: Zero-based index of the item in the store.

    Returns:
        ``{'item': <item>}`` if ``item_id`` is less than the number of stored
        items; otherwise a tuple of ``{'error': 'Item not found'}`` and the
        HTTP status code 404.
    """
    if item_id < len(items):
        return {'item': items[item_id]}
    else:
        return {'error': 'Item not found'}, 404

@app.route('/items', methods=['POST'])
def add_item() -> tuple[dict[str, str], int]:
    """Append the JSON request body to the item store.

    The body is not validated; whatever ``request.get_json()`` returns is
    stored as-is.

    Returns:
        A tuple of ``{'message': 'Item added successfully'}`` and the HTTP
        status code 201.
    """
    item = request.get_json()
    items.append(item)
    return {'message': 'Item added successfully'}, 201
