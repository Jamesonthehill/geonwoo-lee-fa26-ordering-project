import uuid

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel


app = FastAPI(title="Receive an Order Number")


class OrderRequest(BaseModel):
    item: str
    quantity: int


def generate_order_number():
    return "ORD-" + uuid.uuid4().hex[:8].upper()


@app.get("/")
def customer_page():
    return FileResponse("index.html")


@app.post("/orders")
def confirm_order(order: OrderRequest):
    return {
        "message": "Order confirmed",
        "order_number": generate_order_number(),
        "item": order.item,
        "quantity": order.quantity,
    }
