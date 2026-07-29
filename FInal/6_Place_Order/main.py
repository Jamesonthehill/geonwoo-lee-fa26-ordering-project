import sqlite3

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel


app = FastAPI(title="Place Order")


class OrderRequest(BaseModel):
    item_id: int
    quantity: int


def create_tables():
    connection = sqlite3.connect("orders.db")
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS menu (
            id INTEGER PRIMARY KEY,
            name TEXT,
            price REAL,
            available INTEGER
        )
        """
    )
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY,
            total REAL
        )
        """
    )
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY,
            order_id INTEGER,
            item_id INTEGER,
            quantity INTEGER,
            price REAL
        )
        """
    )

    if connection.execute("SELECT COUNT(*) FROM menu").fetchone()[0] == 0:
        connection.executemany(
            "INSERT INTO menu (name, price, available) VALUES (?, ?, ?)",
            [
                ("Avocado Toast", 12.50, 1),
                ("Cafe Latte", 5.50, 1),
                ("Berry Pancakes", 11.00, 0),
            ],
        )

    connection.commit()
    connection.close()


create_tables()


@app.get("/")
def order_page():
    return FileResponse("index.html")


@app.get("/menu")
def get_menu():
    connection = sqlite3.connect("orders.db")
    connection.row_factory = sqlite3.Row
    items = connection.execute("SELECT * FROM menu").fetchall()
    connection.close()
    return [dict(item) for item in items]


@app.post("/orders")
def place_order(order: OrderRequest):
    if order.quantity < 1 or order.quantity > 10:
        raise HTTPException(
            status_code=400, detail="Quantity must be between 1 and 10"
        )

    connection = sqlite3.connect("orders.db")
    connection.row_factory = sqlite3.Row
    item = connection.execute(
        "SELECT * FROM menu WHERE id = ?", (order.item_id,)
    ).fetchone()

    if item is None:
        connection.close()
        raise HTTPException(status_code=404, detail="Item not found")
    if not item["available"]:
        connection.close()
        raise HTTPException(status_code=400, detail="Item is unavailable")

    total = round(item["price"] * order.quantity, 2)
    saved_order = connection.execute(
        "INSERT INTO orders (total) VALUES (?)", (total,)
    )
    connection.execute(
        """
        INSERT INTO order_items (order_id, item_id, quantity, price)
        VALUES (?, ?, ?, ?)
        """,
        (saved_order.lastrowid, item["id"], order.quantity, item["price"]),
    )
    connection.commit()
    connection.close()

    return {"message": "Order saved", "order_id": saved_order.lastrowid, "total": total}
