import os, uuid
import requests
import pytest

BASE = os.environ.get("FT_BASE_URL", "http://localhost:5077")


@pytest.fixture(autouse=True, scope="module")
def _up():
    r = requests.get(BASE + "/", timeout=5)
    assert r.status_code == 200


def test_root():
    r = requests.get(BASE + "/", timeout=5)
    assert r.status_code == 200 and r.text == "Hello, Flask!"


def test_create_and_get_item():
    tag = "ftrun_" + uuid.uuid4().hex[:6]
    r = requests.post(BASE + "/items", json={"name": tag}, timeout=5)
    assert r.status_code == 201
    assert r.json() == {"message": "Item added successfully"}
    items = requests.get(BASE + "/items", timeout=5).json()["items"]
    idx = items.index({"name": tag})
    r = requests.get(f"{BASE}/items/{idx}", timeout=5)
    assert r.status_code == 200 and r.json() == {"item": {"name": tag}}


def test_list_items():
    r = requests.get(BASE + "/items", timeout=5)
    assert r.status_code == 200 and isinstance(r.json()["items"], list)


def test_item_not_found():
    r = requests.get(BASE + "/items/99999", timeout=5)
    assert r.status_code == 404
    assert r.json() == {"error": "Item not found"}


def test_item_invalid_id_type():
    r = requests.get(BASE + "/items/abc", timeout=5)
    assert r.status_code == 404
