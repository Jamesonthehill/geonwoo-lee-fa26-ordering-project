# User Story #6: Place Order

This folder is a standalone FastAPI submission for placing an order.

- `main.py` creates the order and order-item tables, submits an order, and saves it.
- `index.html` contains the customer order form.
- `tests/test_main.py` tests the complete order-submission flow.

## Run

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
uvicorn main:app --reload
```

Open <http://127.0.0.1:8000>.

## Test

```bash
pytest
```
