import sqlite3

import pytest
from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_orders():
    connection = sqlite3.connect("orders.db")
    connection.execute("DELETE FROM order_items")
    connection.execute("DELETE FROM orders")
    connection.commit()
    connection.close()


def test_order_and_order_item_tables_exist():
    connection = sqlite3.connect("orders.db")
    tables = {
        row[0]
        for row in connection.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table'"
        )
    }
    connection.close()
    assert {"orders", "order_items"} <= tables


def test_submit_and_save_order():
    response = client.post("/orders", json={"item_id": 1, "quantity": 2})
    assert response.status_code == 200
    assert response.json()["total"] == 25.00

    connection = sqlite3.connect("orders.db")
    assert connection.execute("SELECT COUNT(*) FROM orders").fetchone()[0] == 1
    assert connection.execute("SELECT COUNT(*) FROM order_items").fetchone()[0] == 1
    connection.close()


def test_unavailable_item_is_rejected():
    response = client.post("/orders", json={"item_id": 3, "quantity": 1})
    assert response.status_code == 400
