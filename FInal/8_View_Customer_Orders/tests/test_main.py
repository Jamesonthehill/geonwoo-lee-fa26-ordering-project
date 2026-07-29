import sqlite3

import pytest
from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_orders():
    connection = sqlite3.connect("orders.db")
    connection.execute("DELETE FROM orders")
    connection.commit()
    connection.close()


def add_test_order():
    return client.post(
        "/orders",
        json={"item": "Avocado Toast", "quantity": 2, "total": 25.00},
    )


def test_manager_endpoint_returns_customer_orders():
    add_test_order()
    response = client.get("/manager/orders")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_order_details_include_number_item_quantity_and_total():
    add_test_order()
    order = client.get("/manager/orders").json()[0]

    assert {"order_number", "item", "quantity", "total"} <= set(order)
    assert order["quantity"] == 2
    assert order["total"] == 25.00


def test_manager_order_history_page():
    response = client.get("/")
    assert response.status_code == 200
    assert "Customer Orders" in response.text
    assert 'id="orders"' in response.text
