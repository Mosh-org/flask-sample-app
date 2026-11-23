import requests
B = "http://localhost:5001"

def test_root():
    r = requests.get(B + "/", timeout=10)
    assert r.status_code == 200 and r.text == "Hello, Flask!"

def test_add_and_get_item():
    r = requests.post(B + "/items", json={"name": "ftrun"}, timeout=10)
    assert r.status_code == 201
    assert r.json() == {"message": "Item added successfully"}
    r = requests.get(B + "/items", timeout=10)
    assert r.status_code == 200 and {"name": "ftrun"} in r.json()["items"]
    r = requests.get(B + "/items/0", timeout=10)
    assert r.status_code == 200 and "item" in r.json()

def test_item_not_found():
    r = requests.get(B + "/items/99999", timeout=10)
    assert r.status_code == 404
    assert r.json() == {"error": "Item not found"}
