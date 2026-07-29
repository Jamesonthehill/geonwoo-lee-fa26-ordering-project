from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_manager_endpoint_returns_customer_orders():
    response = client.get("/manager/orders")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_orders_include_number_item_quantity_and_total():
    order = client.get("/manager/orders").json()[0]

    assert {"order_number", "item", "quantity", "total"} <= set(order)


def test_manager_order_history_page():
    response = client.get("/")

    assert response.status_code == 200
    assert "Customer Orders" in response.text
    assert 'id="orders"' in response.text
