import requests, pytest
BASE = "http://127.0.0.1:5077"

@pytest.fixture(autouse=True, scope="module")
def up():
    requests.get(BASE + "/", timeout=5)

def test_root():
    r = requests.get(BASE + "/", timeout=5)
    assert r.status_code == 200 and r.text == "Hello, Flask!"

def test_add_and_get_item():
    r = requests.post(BASE + "/items", json={"name": "ftrun"}, timeout=5)
    assert r.status_code == 201
    assert r.json() == {"message": "Item added successfully"}
    lst = requests.get(BASE + "/items", timeout=5)
    assert lst.status_code == 200 and {"name": "ftrun"} in lst.json()["items"]
    r = requests.get(BASE + "/items/0", timeout=5)
    assert r.status_code == 200 and "item" in r.json()

def test_item_not_found():
    r = requests.get(BASE + "/items/99999", timeout=5)
    assert r.status_code == 404
    assert r.json() == {"error": "Item not found"}

def test_invalid_item_id_type():
    assert requests.get(BASE + "/items/abc", timeout=5).status_code == 404
