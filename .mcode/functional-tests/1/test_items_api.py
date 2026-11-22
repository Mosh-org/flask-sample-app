"""Functional tests for the Flask sample app items API."""

from __future__ import annotations

import requests
B = "http://localhost:5001"

def test_root() -> None:
    """Verify GET / returns 200 and "Hello, Flask!"."""
    r = requests.get(B + "/", timeout=5)
    assert r.status_code == 200 and r.text == "Hello, Flask!"

def test_list_items() -> None:
    """Verify GET /items returns 200 with an items list."""
    r = requests.get(B + "/items", timeout=5)
    assert r.status_code == 200 and isinstance(r.json()["items"], list)

def test_create_and_get_item() -> None:
    """Verify POST /items creates an item retrievable via GET /items/<id>."""
    item = {"name": "ftrun_widget"}
    r = requests.post(B + "/items", json=item, timeout=5)
    assert r.status_code == 201
    assert r.json() == {"message": "Item added successfully"}
    items = requests.get(B + "/items", timeout=5).json()["items"]
    idx = items.index(item)
    g = requests.get(f"{B}/items/{idx}", timeout=5)
    assert g.status_code == 200 and g.json() == {"item": item}

def test_get_missing_item() -> None:
    """Verify GET of an unknown item index returns 404 with an error body."""
    r = requests.get(B + "/items/99999", timeout=5)
    assert r.status_code == 404 and r.json() == {"error": "Item not found"}

def test_invalid_item_id_type() -> None:
    """Verify a non-integer item id returns 404."""
    assert requests.get(B + "/items/abc", timeout=5).status_code == 404

def test_post_invalid_json() -> None:
    """Verify POST /items with a malformed JSON body returns 400."""
    r = requests.post(B + "/items", data="not json", headers={"Content-Type": "application/json"}, timeout=5)
    assert r.status_code == 400

def test_post_non_json_content_type() -> None:
    """Verify POST /items with a non-JSON content type returns 400 or 415."""
    r = requests.post(B + "/items", data="x", headers={"Content-Type": "text/plain"}, timeout=5)
    assert r.status_code in (400, 415)
