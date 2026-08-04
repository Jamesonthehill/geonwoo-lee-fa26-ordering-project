import sqlite3

from fastapi import FastAPI
from fastapi.responses import FileResponse


app = FastAPI(title="View Customer Orders")


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

    if connection.execute("SELECT COUNT(*) FROM orders").fetchone()[0] == 0:
        connection.executemany(
            """
            INSERT INTO orders (order_number, item, quantity, total)
            VALUES (?, ?, ?, ?)
            """,
            [
                ("ORD-A102B3C4", "Avocado Toast", 2, 25.00),
                ("ORD-D567E8F9", "Cafe Latte", 1, 5.50),
            ],
        )

    connection.commit()
    connection.close()


create_order_table()


@app.get("/")
def manager_page():
    return FileResponse("manager.html")


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
