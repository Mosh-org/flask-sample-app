import os, requests
BASE = f"http://localhost:{os.environ.get('PORT','5001')}"

def test_root_hello():
    r = requests.get(BASE + "/", timeout=10)
    assert r.status_code == 200 and "Hello, Flask!" in r.text

def test_post_then_get_item():
    r = requests.post(BASE + "/items", json={"name": "ftrun_x"}, timeout=10)
    assert r.status_code == 201
    assert r.json() == {"message": "Item added successfully"}
    lst = requests.get(BASE + "/items", timeout=10)
    assert lst.status_code == 200
    items = lst.json()["items"]
    assert {"name": "ftrun_x"} in items
    g = requests.get(BASE + f"/items/{items.index({'name': 'ftrun_x'})}", timeout=10)
    assert g.status_code == 200 and g.json() == {"item": {"name": "ftrun_x"}}

def test_item_not_found():
    r = requests.get(BASE + "/items/99999", timeout=10)
    assert r.status_code == 404
    assert r.json() == {"error": "Item not found"}
