import pytest
from fastapi.testclient import TestClient

from main import app, cart


client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_cart():
    cart.clear()


def add_item(item="Avocado Toast", quantity=1, price=12.50):
    return client.post(
        "/cart",
        json={"item": item, "quantity": quantity, "price": price},
    ).json()


def test_change_quantity_recalculates_total():
    item = add_item()
    response = client.patch(
        f"/cart/{item['id']}",
        json={"quantity": 3},
    )

    assert response.status_code == 200
    assert response.json()["items"][0]["quantity"] == 3
    assert response.json()["subtotal"] == 37.50


def test_remove_item_recalculates_total():
    first = add_item()
    add_item("Cafe Latte", 2, 5.50)
    response = client.delete(f"/cart/{first['id']}")

    assert response.status_code == 200
    assert len(response.json()["items"]) == 1
    assert response.json()["subtotal"] == 11.00


def test_complete_cart_and_order_submission_flow():
    first = add_item()
    second = add_item("Cafe Latte", 1, 5.50)
    client.patch(f"/cart/{first['id']}", json={"quantity": 2})
    client.delete(f"/cart/{second['id']}")

    response = client.post("/submit-order")

    assert response.status_code == 200
    assert response.json()["message"] == "Order submitted"
    assert response.json()["total"] == 25.00
    assert client.get("/cart").json()["items"] == []
