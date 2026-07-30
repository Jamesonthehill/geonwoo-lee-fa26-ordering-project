import pytest
from fastapi.testclient import TestClient

from main import app, cart


client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_cart():
    cart.clear()


def test_cart_starts_empty():
    response = client.get("/cart")
    assert response.json() == {"items": [], "subtotal": 0}


def test_add_selected_item_quantity_and_price():
    response = client.post(
        "/cart",
        json={"item": "Avocado Toast", "quantity": 2, "price": 12.50},
    )
    item = response.json()

    assert response.status_code == 200
    assert item["item"] == "Avocado Toast"
    assert item["quantity"] == 2
    assert item["line_total"] == 25.00


def test_cart_contents_and_subtotal():
    client.post(
        "/cart",
        json={"item": "Avocado Toast", "quantity": 1, "price": 12.50},
    )
    client.post(
        "/cart",
        json={"item": "Cafe Latte", "quantity": 2, "price": 5.50},
    )
    result = client.get("/cart").json()

    assert len(result["items"]) == 2
    assert result["subtotal"] == 23.50
