# tests/test_app.py

from app import routes


def test_items_state_reset_between_tests():
    assert routes.items == []
