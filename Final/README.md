# Sandwich Shop Ordering API

This final sample project provides complete CRUD operations for a sandwich
shop and adds an inventory-aware checkout workflow. It is built with FastAPI,
SQLAlchemy, Pydantic, MySQL, and pytest.

## Features

- CRUD for sandwiches, resources, recipes, orders, and order details
- Order totals through `GET /orders/{order_id}/summary`
- Inventory validation and deduction through
  `POST /orders/{order_id}/checkout`
- Protection against empty orders, missing recipes, insufficient inventory,
  and repeated checkout
- Interactive Swagger documentation
- End-to-end API tests using an isolated SQLite test database

## Project Structure

```text
api/
  controllers/     Database and checkout operations
  dependencies/    Database configuration and sessions
  models/          SQLAlchemy models and Pydantic schemas
  tests/           End-to-end pytest tests
  main.py          FastAPI routes
Documents/         Product backlog, user stories, and sprint backlogs
seed_data.py       Optional presentation data
```

## MySQL Setup

Create a new database in MySQL Workbench:

```sql
CREATE DATABASE IF NOT EXISTS sandwich_shop_final;
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Set your local MySQL credentials:

```bash
export DB_HOST=localhost
export DB_PORT=3306
export DB_NAME=sandwich_shop_final
export DB_USER=root
export DB_PASSWORD='YOUR_MYSQL_PASSWORD'
unset DATABASE_URL
```

## Run The API

```bash
python -m uvicorn api.main:app --reload --port 8080
```

Open `http://127.0.0.1:8080/docs`.

Optional presentation data:

```bash
python seed_data.py
```

## Test

```bash
python -m pytest -q
```

The tests use an isolated SQLite database and do not change MySQL data.

## Demonstration Flow

1. Run `GET /health`.
2. Create or view resources, sandwiches, and recipes.
3. Create an order and an order detail.
4. Run `GET /orders/{order_id}/summary`.
5. Run `POST /orders/{order_id}/checkout`.
6. View the reduced resource amounts.
7. Run `pytest` and show the passing test result.

## Conventional Commit Examples

```text
feat: add sandwich and resource CRUD
feat: add order management endpoints
feat: add inventory-aware checkout
test: cover checkout and CRUD workflows
docs: finalize sprint artifacts and setup guide
```
