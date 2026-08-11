from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel


app = FastAPI(title="Add an Item to the Cart")
cart = []


class CartItem(BaseModel):
    item: str
    quantity: int
    price: float


@app.get("/")
def cart_page():
    return FileResponse("index.html")


@app.post("/cart")
def add_to_cart(item: CartItem):
    if item.quantity < 1:
        raise HTTPException(status_code=400, detail="Quantity must be at least 1")

    cart_item = {
        "id": len(cart) + 1,
        "item": item.item,
        "quantity": item.quantity,
        "price": item.price,
        "line_total": round(item.quantity * item.price, 2),
    }
    cart.append(cart_item)
    return cart_item


@app.get("/cart")
def get_cart():
    return {
        "items": cart,
        "subtotal": round(sum(item["line_total"] for item in cart), 2),
    }
