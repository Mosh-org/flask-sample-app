# tests/test_items.py

import pytest

from app import routes
from app.validation import ItemIn
from pydantic import ValidationError


def assert_error(response, status, code):
    assert response.status_code == status
    assert response.is_json
    body = response.get_json()
    assert set(body) == {'error'}
    assert set(body['error']) == {'code', 'message', 'details'}
    assert body['error']['code'] == code
    assert isinstance(body['error']['details'], list)
    return body['error']


# ---- GET / ----

def test_hello(client):
    r = client.get('/')
    assert (r.status_code, r.text) == (200, "Hello, Flask!")


def test_unknown_route_uniform_404(client):
    assert_error(client.get('/nonexistent'), 404, 'not_found')


def test_wrong_method_uniform_405(client):
    assert_error(client.delete('/items'), 405, 'method_not_allowed')


# ---- GET /items ----

def test_get_items_empty(client):
    r = client.get('/items')
    assert r.status_code == 200
    assert r.headers['Content-Type'] == 'application/json'
    assert r.get_json() == {'items': []}


def test_get_items_after_adds_preserves_order(client):
    client.post('/items', json={'name': 'a'})
    client.post('/items', json={'name': 'b', 'quantity': 3})
    assert client.get('/items').get_json() == {
        'items': [{'name': 'a'}, {'name': 'b', 'quantity': 3}]}


# ---- GET /items/<id> ----

def test_get_item_by_id(client):
    client.post('/items', json={'name': 'a', 'description': 'd'})
    r = client.get('/items/0')
    assert r.status_code == 200
    assert r.get_json() == {'item': {'name': 'a', 'description': 'd'}}


def test_get_item_last_index_and_one_past(client):
    client.post('/items', json={'name': 'a'})
    client.post('/items', json={'name': 'b'})
    assert client.get('/items/1').status_code == 200
    err = assert_error(client.get('/items/2'), 404, 'not_found')
    assert err['message'] == 'Item not found'


def test_get_item_empty_store(client):
    assert_error(client.get('/items/0'), 404, 'not_found')


def test_get_item_large_id(client):
    assert_error(client.get('/items/999999999999'), 404, 'not_found')


def test_get_item_negative_id_not_routed(client):
    assert_error(client.get('/items/-1'), 404, 'not_found')


def test_get_item_non_integer_id(client):
    assert_error(client.get('/items/abc'), 404, 'not_found')


# ---- POST /items happy paths ----

def test_add_item_minimal(client):
    r = client.post('/items', json={'name': 'x'})
    assert r.status_code == 201
    assert r.get_json() == {'message': 'Item added successfully'}
    assert routes.items == [{'name': 'x'}]


def test_add_item_full(client):
    body = {'name': 'x', 'description': 'desc', 'quantity': 5}
    assert client.post('/items', json=body).status_code == 201
    assert routes.items == [body]


def test_add_item_content_type_with_charset(client):
    r = client.post('/items', data='{"name": "x"}',
                    content_type='application/json; charset=utf-8')
    assert r.status_code == 201


def test_add_item_strips_name_whitespace(client):
    client.post('/items', json={'name': '  padded  '})
    assert routes.items == [{'name': 'padded'}]


def test_add_item_null_optionals_dropped(client):
    client.post('/items', json={'name': 'x', 'description': None, 'quantity': None})
    assert routes.items == [{'name': 'x'}]


@pytest.mark.parametrize('body', [
    {'name': 'n'},
    {'name': 'n' * 100},
    {'name': 'x', 'description': 'd' * 500},
    {'name': 'x', 'description': ''},
    {'name': 'x', 'quantity': 0},
    {'name': 'x', 'quantity': 1_000_000},
])
def test_boundaries_accepted(client, body):
    assert client.post('/items', json=body).status_code == 201


# ---- POST /items failures ----

def test_missing_content_type_415(client):
    r = client.post('/items', data='{"name": "x"}')
    assert_error(r, 415, 'unsupported_media_type')
    assert routes.items == []


def test_wrong_content_type_415(client):
    r = client.post('/items', data='name=x', content_type='text/plain')
    assert_error(r, 415, 'unsupported_media_type')


@pytest.mark.parametrize('raw', ['{bad', '', '{"name": ', "{'name': 'x'}"])
def test_malformed_json_400(client, raw):
    r = client.post('/items', data=raw, content_type='application/json')
    assert_error(r, 400, 'malformed_json')
    assert routes.items == []


@pytest.mark.parametrize('raw', ['null', '[]', '[{"name": "x"}]', '"str"', '42', 'true'])
def test_non_object_body_422(client, raw):
    r = client.post('/items', data=raw, content_type='application/json')
    assert_error(r, 422, 'validation_error')
    assert routes.items == []


def test_empty_object_missing_name(client):
    err = assert_error(client.post('/items', json={}), 422, 'validation_error')
    assert err['details'][0]['loc'] == ['name']


@pytest.mark.parametrize('body, field', [
    ({'name': ''}, 'name'),
    ({'name': '   '}, 'name'),
    ({'name': 'n' * 101}, 'name'),
    ({'name': 123}, 'name'),
    ({'name': None}, 'name'),
    ({'name': 'x', 'description': 'd' * 501}, 'description'),
    ({'name': 'x', 'description': 5}, 'description'),
    ({'name': 'x', 'quantity': -1}, 'quantity'),
    ({'name': 'x', 'quantity': 1_000_001}, 'quantity'),
    ({'name': 'x', 'quantity': '5'}, 'quantity'),
    ({'name': 'x', 'quantity': 1.5}, 'quantity'),
    ({'name': 'x', 'quantity': True}, 'quantity'),
    ({'name': 'x', 'extra': 1}, 'extra'),
])
def test_field_validation_failures(client, body, field):
    err = assert_error(client.post('/items', json=body), 422, 'validation_error')
    assert err['details'][0]['loc'] == [field]
    assert routes.items == []


def test_multiple_errors_reported(client):
    err = assert_error(client.post('/items', json={'name': '', 'quantity': -1}),
                       422, 'validation_error')
    assert len(err['details']) == 2


# ---- ItemIn model ----

def test_itemin_valid():
    assert ItemIn(name='a').model_dump(exclude_none=True) == {'name': 'a'}


def test_itemin_invalid():
    with pytest.raises(ValidationError):
        ItemIn(name='')


# ---- Central handlers ----

def test_unexpected_exception_uniform_500(client, monkeypatch):
    def boom(*a, **k):
        raise RuntimeError('boom')
    monkeypatch.setattr(routes, 'ItemIn', type('X', (), {'model_validate': staticmethod(boom)}))
    from app import app
    app.config['PROPAGATE_EXCEPTIONS'] = False
    r = client.post('/items', json={'name': 'x'})
    err = assert_error(r, 500, 'internal_error')
    assert 'boom' not in err['message']
