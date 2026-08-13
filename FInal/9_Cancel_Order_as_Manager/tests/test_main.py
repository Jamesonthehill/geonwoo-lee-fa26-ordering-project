import sqlite3

import pytest
from fastapi.testclient import TestClient

from main import DATABASE, app


client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_order_statuses():
    connection = sqlite3.connect(DATABASE)
    connection.execute("UPDATE orders SET status = 'Confirmed'")
    connection.commit()
    connection.close()


def test_manager_can_view_order_status():
    response = client.get("/manager/orders")

    assert response.status_code == 200
    assert response.json()[0]["status"] == "Confirmed"


def test_manager_can_cancel_order():
    response = client.patch("/manager/orders/ORD-A102B3C4/cancel")

    assert response.status_code == 200
    assert response.json()["status"] == "Cancelled"


def test_cancelled_status_is_saved():
    client.patch("/manager/orders/ORD-A102B3C4/cancel")
    orders = client.get("/manager/orders").json()
    cancelled = next(
        order for order in orders if order["order_number"] == "ORD-A102B3C4"
    )

    assert cancelled["status"] == "Cancelled"


def test_order_cannot_be_cancelled_twice():
    client.patch("/manager/orders/ORD-A102B3C4/cancel")
    response = client.patch("/manager/orders/ORD-A102B3C4/cancel")

    assert response.status_code == 400
