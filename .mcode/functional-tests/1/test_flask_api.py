import requests

BASE = "http://localhost:5001"


def test_index():
    r = requests.get(BASE + "/", timeout=10)
    assert r.status_code == 200
    assert "Hello, Flask!" in r.text


def test_list_items():
    r = requests.get(BASE + "/items", timeout=10)
    assert r.status_code == 200
    assert isinstance(r.json()["items"], list)


def test_add_then_get_item():
    before = requests.get(BASE + "/items", timeout=10).json()["items"]
    r = requests.post(BASE + "/items", json={"name": "ftrun_item"}, timeout=10)
    assert r.status_code == 201
    assert r.json() == {"message": "Item added successfully"}
    after = requests.get(BASE + "/items", timeout=10).json()["items"]
    assert len(after) == len(before) + 1
    g = requests.get(BASE + "/items/%d" % (len(after) - 1), timeout=10)
    assert g.status_code == 200
    assert g.json() == {"item": {"name": "ftrun_item"}}


def test_item_out_of_range():
    n = len(requests.get(BASE + "/items", timeout=10).json()["items"])
    r = requests.get(BASE + "/items/%d" % (n + 100), timeout=10)
    assert r.status_code == 404
    assert r.json() == {"error": "Item not found"}


def test_negative_index_404():
    r = requests.get(BASE + "/items/-1", timeout=10)
    assert r.status_code == 404
