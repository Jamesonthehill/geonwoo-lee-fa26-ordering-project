# CRUD FastAPI Sandwich Maker

This project implements CRUD operations for all five tables required by the
assignment:

- `orders`
- `sandwiches`
- `resources`
- `recipes`
- `order_details`

Each table has create, read-all, read-one, update, and delete operations.

## MySQL Setup

Create the required database in MySQL Workbench:

```sql
CREATE DATABASE sandwich_maker_api;
```

Create and activate a virtual environment, then install the packages:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Set your MySQL credentials before starting the API:

```bash
export DB_HOST=localhost
export DB_PORT=3306
export DB_NAME=sandwich_maker_api
export DB_USER=root
export DB_PASSWORD=YOUR_PASSWORD
```

Run the application from the project directory:

```bash
uvicorn api.main:app --reload
```

SQLAlchemy will create the five tables automatically. Open Swagger UI at:

```text
http://127.0.0.1:8000/docs
```

## Testing Order

Foreign keys mean the easiest Swagger testing order is:

1. Create resources.
2. Create sandwiches.
3. Create recipes using the new resource and sandwich IDs.
4. Create an order.
5. Create order details using the new order and sandwich IDs.
6. Test read-all, read-one, update, and delete for each group.

For local testing without MySQL, the project also accepts a SQLAlchemy URL:

```bash
DATABASE_URL=sqlite:///./sandwich_maker_api.db uvicorn api.main:app --reload
```
