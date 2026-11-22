# app/routes.py

from app import app
from typing import Any, Dict, Tuple, Union

from flask import request

items = []

@app.route('/')
def hello() -> str:
    """Return a greeting."""
    return "Hello, Flask!"

@app.route('/items', methods=['GET'])
def get_items() -> Dict[str, Any]:
    """Return all stored items."""
    return {'items': items}

@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id: int) -> Union[Dict[str, Any], Tuple[Dict[str, Any], int]]:
    """Return the item at item_id, or a 404 error."""
    if item_id < len(items):
        return {'item': items[item_id]}
    else:
        return {'error': 'Item not found'}, 404

@app.route('/items', methods=['POST'])
def add_item() -> Tuple[Dict[str, Any], int]:
    """Store the posted JSON item and return 201."""
    item = request.get_json()
    items.append(item)
    return {'message': 'Item added successfully'}, 201
