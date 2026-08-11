import sqlite3

from fastapi import FastAPI
from fastapi.responses import FileResponse


app = FastAPI(title="Cafe Menu")


def create_menu_table():
    connection = sqlite3.connect("menu.db")
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS menu (
            id INTEGER PRIMARY KEY,
            name TEXT,
            price REAL,
            picture TEXT,
            available INTEGER
        )
        """
    )

    if connection.execute("SELECT COUNT(*) FROM menu").fetchone()[0] == 0:
        sample_menu = [
            (
                "Avocado Toast",
                12.50,
                "https://images.unsplash.com/photo-1541519227354-08fa5d50c44d?w=600",
                1,
            ),
            (
                "Cafe Latte",
                5.50,
                "https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=600",
                1,
            ),
            (
                "Berry Pancakes",
                11.00,
                "https://images.unsplash.com/photo-1528207776546-365bb710ee93?w=600",
                0,
            ),
        ]
        connection.executemany(
            "INSERT INTO menu (name, price, picture, available) VALUES (?, ?, ?, ?)",
            sample_menu,
        )

    connection.commit()
    connection.close()


create_menu_table()


@app.get("/")
def show_menu_page():
    return FileResponse("index.html")


@app.get("/menu")
def get_menu():
    connection = sqlite3.connect("menu.db")
    connection.row_factory = sqlite3.Row
    items = connection.execute("SELECT * FROM menu").fetchall()
    connection.close()
    return [dict(item) for item in items]
