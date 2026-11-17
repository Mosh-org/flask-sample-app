import os
import pytest
import requests

BASE = "http://localhost:%s" % os.environ.get("PORT", "5001")
T = 10


def post(body=None, **kw):
    return requests.post(BASE + "/items", timeout=T, **kw)


def err(r):
    e = r.json()["error"]
    assert set(e) >= {"code", "message", "details"}
    return e


def test_root():
    r = requests.get(BASE + "/", timeout=T)
    assert r.status_code == 200 and r.text == "Hello, Flask!"


def test_create_item_happy():
    r = post(json={"name": "widget", "description": "d", "quantity": 5})
    assert r.status_code == 201
    assert r.json() == {"message": "Item added successfully"}


def test_create_item_name_only():
    assert post(json={"name": "x"}).status_code == 201


def test_list_and_get_item():
    name = "ftlist"
    assert post(json={"name": name}).status_code == 201
    items = requests.get(BASE + "/items", timeout=T).json()["items"]
    assert any(i["name"] == name for i in items)
    idx = [i["name"] for i in items].index(name)
    r = requests.get(BASE + "/items/%d" % idx, timeout=T)
    assert r.status_code == 200 and r.json()["item"]["name"] == name


def test_get_item_out_of_range():
    r = requests.get(BASE + "/items/999999", timeout=T)
    assert r.status_code == 404
    assert err(r)["code"] == "not_found"


def test_get_item_negative_id():
    r = requests.get(BASE + "/items/-1", timeout=T)
    assert r.status_code == 404
    err(r)


def test_non_json_content_type():
    r = post(data="name=x", headers={"Content-Type": "text/plain"})
    assert r.status_code == 415
    err(r)


def test_malformed_json():
    r = post(data="{bad", headers={"Content-Type": "application/json"})
    assert r.status_code == 400
    err(r)


def test_missing_name():
    r = post(json={"description": "x"})
    assert r.status_code == 422
    assert err(r)["details"]


@pytest.mark.parametrize("body", [
    {"name": ""},
    {"name": "a" * 101},
    {"name": "ok", "description": "d" * 501},
    {"name": "ok", "quantity": -1},
    {"name": "ok", "quantity": 1000001},
    {"name": "ok", "quantity": "5"},
    {"name": 123},
    {"name": "ok", "extra": 1},
    [1, 2],
])
def test_validation_failures(body):
    r = post(json=body)
    assert r.status_code == 422
    err(r)


@pytest.mark.parametrize("body", [
    {"name": "a" * 100},
    {"name": "ok", "description": "d" * 500},
    {"name": "ok", "quantity": 0},
    {"name": "ok", "quantity": 1000000},
])
def test_boundaries_ok(body):
    assert post(json=body).status_code == 201


def test_unknown_route_uniform_error():
    r = requests.get(BASE + "/nope", timeout=T)
    assert r.status_code == 404
    err(r)
