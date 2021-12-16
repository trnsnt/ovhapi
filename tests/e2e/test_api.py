from fastapi.testclient import TestClient

from ovhapi import __version__
from ovhapi.main import app
from ovhapi.core.config import settings

client = TestClient(app)


def test_version():
    assert __version__ == "0.1.0"


def test_hello():
    response = client.get("/")
    assert response.json() == f"Welcome to {settings.PROJECT_NAME}"
