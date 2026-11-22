import os, requests
BASE = f"http://localhost:{os.environ.get('PORT','5001')}"

def test_hello():
    r = requests.get(BASE + "/", timeout=5)
    assert r.status_code == 200 and r.text == "Hello, Flask!"

def test_get_items():
    r = requests.get(BASE + "/items", timeout=5)
    assert r.status_code == 200 and isinstance(r.json()["items"], list)

def test_get_item_missing():
    r = requests.get(BASE + "/items/999999", timeout=5)
    assert r.status_code == 404 and r.json() == {"error": "Item not found"}

def test_add_and_get_item():
    n = len(requests.get(BASE + "/items", timeout=5).json()["items"])
    r = requests.post(BASE + "/items", json={"name": "ftrun_x"}, timeout=5)
    assert r.status_code == 201 and r.json() == {"message": "Item added successfully"}
    g = requests.get(f"{BASE}/items/{n}", timeout=5)
    assert g.status_code == 200 and g.json() == {"item": {"name": "ftrun_x"}}
