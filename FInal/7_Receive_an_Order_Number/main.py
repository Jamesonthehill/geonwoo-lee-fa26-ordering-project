import sqlite3
import uuid

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel


app = FastAPI(title="Receive an Order Number")


class OrderRequest(BaseModel):
    item: str
    quantity: int
    total: float


def create_order_table():
    connection = sqlite3.connect("orders.db")
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY,
            order_number TEXT UNIQUE,
            item TEXT,
            quantity INTEGER,
            total REAL
        )
        """
    )
    connection.commit()
    connection.close()


def generate_order_number():
    return "ORD-" + uuid.uuid4().hex[:8].upper()


create_order_table()


@app.get("/")
def confirmation_page():
    return FileResponse("index.html")


@app.post("/orders")
def confirm_order(order: OrderRequest):
    order_number = generate_order_number()
    connection = sqlite3.connect("orders.db")
    connection.execute(
        """
        INSERT INTO orders (order_number, item, quantity, total)
        VALUES (?, ?, ?, ?)
        """,
        (order_number, order.item, order.quantity, order.total),
    )
    connection.commit()
    connection.close()

    return {
        "message": "Order confirmed",
        "order_number": order_number,
    }
