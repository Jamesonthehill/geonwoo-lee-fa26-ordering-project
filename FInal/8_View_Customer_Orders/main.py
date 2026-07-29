import sqlite3
import uuid

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel


app = FastAPI(title="View Customer Orders")


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


create_order_table()


@app.get("/")
def manager_page():
    return FileResponse("manager.html")


@app.post("/orders")
def create_test_order(order: OrderRequest):
    order_number = "ORD-" + uuid.uuid4().hex[:8].upper()
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
    return {"order_number": order_number}


@app.get("/manager/orders")
def get_customer_orders():
    connection = sqlite3.connect("orders.db")
    connection.row_factory = sqlite3.Row
    orders = connection.execute(
        """
        SELECT order_number, item, quantity, total
        FROM orders
        ORDER BY id DESC
        """
    ).fetchall()
    connection.close()
    return [dict(order) for order in orders]
