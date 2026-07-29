def create_catalog(client, resource_amount=20):
    resource = client.post(
        "/resources/",
        json={"item": "bread", "amount": resource_amount},
    )
    assert resource.status_code == 200

    sandwich = client.post(
        "/sandwiches/",
        json={"sandwich_name": "Ham Sandwich", "price": 5.5},
    )
    assert sandwich.status_code == 200

    recipe = client.post(
        "/recipes/",
        json={
            "sandwich_id": sandwich.json()["id"],
            "resource_id": resource.json()["id"],
            "amount": 2,
        },
    )
    assert recipe.status_code == 200
    return resource.json(), sandwich.json()


def create_order_with_item(client, sandwich_id, quantity=2):
    order = client.post(
        "/orders/",
        json={"customer_name": "Jamie", "description": "Lunch order"},
    )
    assert order.status_code == 200

    detail = client.post(
        "/order_details/",
        json={
            "order_id": order.json()["id"],
            "sandwich_id": sandwich_id,
            "amount": quantity,
        },
    )
    assert detail.status_code == 200
    return order.json()


def test_sandwich_crud(client):
    created = client.post(
        "/sandwiches/",
        json={"sandwich_name": "Veggie", "price": 4.25},
    )
    assert created.status_code == 200
    sandwich_id = created.json()["id"]

    read = client.get(f"/sandwiches/{sandwich_id}")
    assert read.status_code == 200
    assert read.json()["sandwich_name"] == "Veggie"

    updated = client.put(
        f"/sandwiches/{sandwich_id}",
        json={"price": 4.75},
    )
    assert updated.status_code == 200
    assert updated.json()["price"] == 4.75

    deleted = client.delete(f"/sandwiches/{sandwich_id}")
    assert deleted.status_code == 204
    assert client.get(f"/sandwiches/{sandwich_id}").status_code == 404


def test_checkout_calculates_total_and_reduces_inventory(client):
    resource, sandwich = create_catalog(client)
    order = create_order_with_item(client, sandwich["id"], quantity=2)

    response = client.post(f"/orders/{order['id']}/checkout")

    assert response.status_code == 200
    assert response.json()["status"] == "completed"
    assert response.json()["total"] == 11.0
    assert response.json()["items"][0]["quantity"] == 2

    remaining = client.get(f"/resources/{resource['id']}")
    assert remaining.json()["amount"] == 16

    repeated = client.post(f"/orders/{order['id']}/checkout")
    assert repeated.status_code == 409


def test_checkout_rejects_insufficient_inventory(client):
    resource, sandwich = create_catalog(client, resource_amount=3)
    order = create_order_with_item(client, sandwich["id"], quantity=2)

    response = client.post(f"/orders/{order['id']}/checkout")

    assert response.status_code == 409
    assert "Insufficient resources" in response.json()["detail"]
    remaining = client.get(f"/resources/{resource['id']}")
    assert remaining.json()["amount"] == 3


def test_related_table_crud_workflow(client):
    resource, sandwich = create_catalog(client)
    recipe = client.get("/recipes/").json()[0]
    order = create_order_with_item(client, sandwich["id"], quantity=1)
    detail = client.get("/order_details/").json()[0]

    assert client.get(f"/recipes/{recipe['id']}").status_code == 200
    assert client.get(f"/orders/{order['id']}").status_code == 200
    assert client.get(f"/order_details/{detail['id']}").status_code == 200

    assert client.put(
        f"/resources/{resource['id']}",
        json={"amount": 25},
    ).json()["amount"] == 25
    assert client.put(
        f"/recipes/{recipe['id']}",
        json={"amount": 3},
    ).json()["amount"] == 3
    assert client.put(
        f"/orders/{order['id']}",
        json={"description": "Updated lunch order"},
    ).json()["description"] == "Updated lunch order"
    assert client.put(
        f"/order_details/{detail['id']}",
        json={"amount": 2},
    ).json()["amount"] == 2

    assert client.delete(f"/order_details/{detail['id']}").status_code == 204
    assert client.delete(f"/recipes/{recipe['id']}").status_code == 204
    assert client.delete(f"/orders/{order['id']}").status_code == 204
    assert client.delete(f"/sandwiches/{sandwich['id']}").status_code == 204
    assert client.delete(f"/resources/{resource['id']}").status_code == 204
