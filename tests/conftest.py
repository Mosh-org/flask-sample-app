# tests/conftest.py

import os
import tempfile

# Keep logging hermetic: must be set before `app` is imported.
os.environ.setdefault("FLASK_SAMPLE_APP_LOG_DIR", tempfile.mkdtemp(prefix="flask_sample_app_logs_"))

import pytest

from app import app as flask_app
from app import routes


@pytest.fixture(autouse=True)
def clean_items():
    routes.items.clear()
    yield
    routes.items.clear()


@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    return flask_app.test_client()
