from fastapi.testclient import TestClient

from main import app, generate_order_number


client = TestClient(app)


def test_order_number_is_unique():
    assert generate_order_number() != generate_order_number()


def test_fastapi_returns_confirmation_and_order_number():
    response = client.post(
        "/orders",
        json={"item": "Avocado Toast", "quantity": 2},
    )
    order = response.json()

    assert response.status_code == 200
    assert order["message"] == "Order confirmed"
    assert order["order_number"].startswith("ORD-")


def test_customer_page_displays_confirmation_area():
    response = client.get("/")

    assert response.status_code == 200
    assert 'id="confirmation"' in response.text
