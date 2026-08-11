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


def test_select_item_and_quantity():
    response = client.get("/selection/1?quantity=2")
    assert response.status_code == 200
    assert response.json()["quantity"] == 2
    assert response.json()["total"] == 25.00


def test_invalid_quantity():
    response = client.get("/selection/1?quantity=0")
    assert response.status_code == 422


def test_unavailable_item_cannot_be_selected():
    response = client.get("/selection/3?quantity=1")
    assert response.status_code == 400
