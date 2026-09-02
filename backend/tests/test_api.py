import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_home_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert "AutoSecAI" in response.json()["message"]


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "Running Successfully"


def test_auth_me_unauthorized():
    response = client.get("/auth/me")
    assert response.status_code == 401
