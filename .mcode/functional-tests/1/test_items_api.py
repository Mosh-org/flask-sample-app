import os
import requests

BASE = f"http://localhost:{os.environ.get('PORT', '5001')}"


def test_hello():
    r = requests.get(f"{BASE}/", timeout=10)
    assert r.status_code == 200 and r.text == "Hello, Flask!"


def test_get_items_list():
    r = requests.get(f"{BASE}/items", timeout=10)
    assert r.status_code == 200 and isinstance(r.json()["items"], list)


def test_post_then_get_item():
    n = len(requests.get(f"{BASE}/items", timeout=10).json()["items"])
    body = {"name": "ftrun_widget"}
    r = requests.post(f"{BASE}/items", json=body, timeout=10)
    assert r.status_code == 201
    assert r.json() == {"message": "Item added successfully"}
    g = requests.get(f"{BASE}/items/{n}", timeout=10)
    assert g.status_code == 200 and g.json() == {"item": body}


def test_get_missing_item_404():
    r = requests.get(f"{BASE}/items/99999", timeout=10)
    assert r.status_code == 404 and r.json() == {"error": "Item not found"}


def test_non_integer_item_id_404():
    assert requests.get(f"{BASE}/items/abc", timeout=10).status_code == 404
