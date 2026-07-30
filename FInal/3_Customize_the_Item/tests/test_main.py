from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_small_size_price():
    response = client.post(
        "/customize",
        json={"size": "small", "ingredients": []},
    )
    assert response.status_code == 200
    assert response.json()["price"] == 8.00


def test_large_size_updates_price():
    response = client.post(
        "/customize",
        json={"size": "large", "ingredients": []},
    )
    assert response.json()["price"] == 11.00


def test_adding_and_removing_ingredients_updates_price():
    with_ingredients = client.post(
        "/customize",
        json={"size": "medium", "ingredients": ["cheese", "avocado"]},
    ).json()
    without_ingredients = client.post(
        "/customize",
        json={"size": "medium", "ingredients": []},
    ).json()

    assert with_ingredients["price"] == 12.50
    assert without_ingredients["price"] == 9.50


def test_invalid_size_is_rejected():
    response = client.post(
        "/customize",
        json={"size": "extra-large", "ingredients": []},
    )
    assert response.status_code == 400
