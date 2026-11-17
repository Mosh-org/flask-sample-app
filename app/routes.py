# app/routes.py

from app import app
from app.errors import ApiError, error_detail, validation_details
from app.validation import ItemIn
from flask import request
from pydantic import ValidationError

items = []

@app.route('/')
def hello():
    return "Hello, Flask!"

@app.route('/items', methods=['GET'])
def get_items():
    return {'items': items}

@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    if 0 <= item_id < len(items):
        return {'item': items[item_id]}
    raise ApiError(404, 'not_found', 'Item not found')

@app.route('/items', methods=['POST'])
def add_item():
    if not request.is_json:
        raise ApiError(415, 'unsupported_media_type',
                       'Content-Type must be application/json')
    payload = request.get_json(silent=True)
    if payload is None and request.get_data(cache=True).strip() != b'null':
        raise ApiError(400, 'malformed_json', 'Request body is not valid JSON')
    if not isinstance(payload, dict):
        raise ApiError(422, 'validation_error', 'Request body must be a JSON object',
                       [error_detail([], 'must be a JSON object', 'object_type')])
    try:
        item = ItemIn.model_validate(payload)
    except ValidationError as exc:
        raise ApiError(422, 'validation_error', 'Invalid item',
                       validation_details(exc.errors()))
    items.append(item.model_dump(exclude_none=True))
    return {'message': 'Item added successfully'}, 201
