import sqlite3

import pytest
from fastapi.testclient import TestClient

from main import app, generate_order_number


client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_orders():
    connection = sqlite3.connect("orders.db")
    connection.execute("DELETE FROM orders")
    connection.commit()
    connection.close()


def test_unique_order_numbers():
    assert generate_order_number() != generate_order_number()


def test_api_returns_order_number_and_confirmation():
    response = client.post(
        "/orders",
        json={"item": "Cafe Latte", "quantity": 2, "total": 11.00},
    )
    result = response.json()

    assert response.status_code == 200
    assert result["message"] == "Order confirmed"
    assert result["order_number"].startswith("ORD-")


def test_confirmation_page():
    response = client.get("/")
    assert response.status_code == 200
    assert 'id="confirmation"' in response.text
