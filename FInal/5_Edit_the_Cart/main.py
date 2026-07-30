from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel


app = FastAPI(title="Edit the Cart")
cart = []


class CartItem(BaseModel):
    item: str
    quantity: int
    price: float


class QuantityUpdate(BaseModel):
    quantity: int


def cart_response():
    return {
        "items": cart,
        "subtotal": round(sum(item["line_total"] for item in cart), 2),
    }


def find_cart_item(item_id):
    return next((item for item in cart if item["id"] == item_id), None)


@app.get("/")
def cart_page():
    return FileResponse("index.html")


@app.get("/cart")
def get_cart():
    return cart_response()


@app.post("/cart")
def add_to_cart(item: CartItem):
    if item.quantity < 1:
        raise HTTPException(status_code=400, detail="Quantity must be at least 1")

    new_item = {
        "id": max((cart_item["id"] for cart_item in cart), default=0) + 1,
        "item": item.item,
        "quantity": item.quantity,
        "price": item.price,
        "line_total": round(item.quantity * item.price, 2),
    }
    cart.append(new_item)
    return new_item


@app.patch("/cart/{item_id}")
def change_quantity(item_id: int, update: QuantityUpdate):
    if update.quantity < 1:
        raise HTTPException(status_code=400, detail="Quantity must be at least 1")

    item = find_cart_item(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Cart item not found")

    item["quantity"] = update.quantity
    item["line_total"] = round(item["price"] * update.quantity, 2)
    return cart_response()


@app.delete("/cart/{item_id}")
def remove_item(item_id: int):
    item = find_cart_item(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Cart item not found")

    cart.remove(item)
    return cart_response()


@app.post("/submit-order")
def submit_order():
    if not cart:
        raise HTTPException(status_code=400, detail="Cart is empty")

    order = {
        "message": "Order submitted",
        "items": list(cart),
        "total": cart_response()["subtotal"],
    }
    cart.clear()
    return order
