import pytest
from fastapi.testclient import TestClient

from app import app
import os


@pytest.fixture
def client():
    yield TestClient(app)


def pytest_sessionfinish(session, exitstatus):
    app.container.db()._engine.dispose()
    os.remove("test.db")
