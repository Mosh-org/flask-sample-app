import os
import requests

BASE = f"http://localhost:{os.environ.get('PORT', '5001')}"


def test_hello():
    r = requests.get(f"{BASE}/", timeout=5)
    assert r.status_code == 200
    assert r.text == "Hello, Flask!"


def test_add_then_read_item():
    before = requests.get(f"{BASE}/items", timeout=5).json()["items"]
    idx = len(before)
    r = requests.post(f"{BASE}/items", json={"name": "ftrun_widget"}, timeout=5)
    assert r.status_code == 201
    assert r.json() == {"message": "Item added successfully"}
    items = requests.get(f"{BASE}/items", timeout=5)
    assert items.status_code == 200
    assert items.json()["items"][idx] == {"name": "ftrun_widget"}
    one = requests.get(f"{BASE}/items/{idx}", timeout=5)
    assert one.status_code == 200
    assert one.json() == {"item": {"name": "ftrun_widget"}}


def test_get_first_item():
    if not requests.get(f"{BASE}/items", timeout=5).json()["items"]:
        requests.post(f"{BASE}/items", json={"name": "ftrun_first"}, timeout=5)
    r = requests.get(f"{BASE}/items/0", timeout=5)
    assert r.status_code == 200
    assert "item" in r.json()


def test_item_not_found():
    r = requests.get(f"{BASE}/items/999999", timeout=5)
    assert r.status_code == 404
    assert r.json() == {"error": "Item not found"}


def test_item_non_int_id():
    r = requests.get(f"{BASE}/items/abc", timeout=5)
    assert r.status_code == 404
