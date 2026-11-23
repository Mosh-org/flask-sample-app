import os
import requests

BASE = f"http://localhost:{os.environ.get('PORT', '5001')}"
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))


def test_contributing_md_exists():
    p = os.path.join(REPO, "CONTRIBUTING.md")
    assert os.path.isfile(p)
    assert os.path.getsize(p) > 0


def test_list_items():
    r = requests.get(f"{BASE}/items", timeout=10)
    assert r.status_code == 200
    assert isinstance(r.json()["items"], list)


def test_add_and_get_item():
    r = requests.post(f"{BASE}/items", json={"name": "ftrun_widget"}, timeout=10)
    assert r.status_code == 201
    assert r.json() == {"message": "Item added successfully"}
    items = requests.get(f"{BASE}/items", timeout=10).json()["items"]
    idx = items.index({"name": "ftrun_widget"})
    g = requests.get(f"{BASE}/items/{idx}", timeout=10)
    assert g.status_code == 200
    assert g.json() == {"item": {"name": "ftrun_widget"}}


def test_item_not_found():
    r = requests.get(f"{BASE}/items/99999", timeout=10)
    assert r.status_code == 404
    assert r.json() == {"error": "Item not found"}


def test_invalid_item_id_type():
    assert requests.get(f"{BASE}/items/abc", timeout=10).status_code == 404
