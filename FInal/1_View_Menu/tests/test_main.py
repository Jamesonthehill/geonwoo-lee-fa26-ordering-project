from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_menu_endpoint():
    response = client.get("/menu")
    assert response.status_code == 200
    assert len(response.json()) == 3


def test_available_item():
    items = client.get("/menu").json()
    assert any(item["available"] == 1 for item in items)


def test_unavailable_item():
    items = client.get("/menu").json()
    assert any(item["available"] == 0 for item in items)
