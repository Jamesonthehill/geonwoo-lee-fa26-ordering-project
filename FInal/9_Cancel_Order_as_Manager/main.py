import sqlite3
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse


FOLDER = Path(__file__).resolve().parent
DATABASE = FOLDER / "orders.db"

app = FastAPI(title="Cancel Order as Manager")


def connect():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def create_order_table():
    connection = connect()
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY,
            order_number TEXT UNIQUE,
            item TEXT,
            quantity INTEGER,
            total REAL,
            status TEXT NOT NULL DEFAULT 'Confirmed'
        )
        """
    )

    if connection.execute("SELECT COUNT(*) FROM orders").fetchone()[0] == 0:
        connection.executemany(
            """
            INSERT INTO orders
                (order_number, item, quantity, total, status)
            VALUES (?, ?, ?, ?, ?)
            """,
            [
                ("ORD-A102B3C4", "Avocado Toast", 2, 25.00, "Confirmed"),
                ("ORD-D567E8F9", "Cafe Latte", 1, 5.50, "Confirmed"),
            ],
        )

    connection.commit()
    connection.close()


create_order_table()


@app.get("/")
def manager_page():
    return FileResponse(FOLDER / "manager.html")


@app.get("/manager/orders")
def get_orders():
    connection = connect()
    orders = connection.execute(
        """
        SELECT order_number, item, quantity, total, status
        FROM orders
        ORDER BY id DESC
        """
    ).fetchall()
    connection.close()
    return [dict(order) for order in orders]


@app.patch("/manager/orders/{order_number}/cancel")
def cancel_order(order_number: str):
    connection = connect()
    order = connection.execute(
        "SELECT status FROM orders WHERE order_number = ?",
        (order_number,),
    ).fetchone()

    if order is None:
        connection.close()
        raise HTTPException(status_code=404, detail="Order not found")
    if order["status"] == "Cancelled":
        connection.close()
        raise HTTPException(status_code=400, detail="Order is already cancelled")

    connection.execute(
        "UPDATE orders SET status = 'Cancelled' WHERE order_number = ?",
        (order_number,),
    )
    connection.commit()
    connection.close()

    return {
        "message": "Order cancelled",
        "order_number": order_number,
        "status": "Cancelled",
    }
