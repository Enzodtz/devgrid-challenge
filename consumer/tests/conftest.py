from app import container
import os


def pytest_sessionfinish(session, exitstatus):
    container.db()._engine.dispose()
    os.remove("test.db")
