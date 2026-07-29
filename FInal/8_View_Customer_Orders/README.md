# User Story #8: View Customer Orders

This folder is a standalone FastAPI submission for the manager order history.

- `main.py` saves test orders and provides the manager orders endpoint.
- `manager.html` displays order numbers, items, quantities, and totals.
- `tests/test_main.py` tests the endpoint, returned details, and manager page.

## Run

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
uvicorn main:app --reload
```

Open <http://127.0.0.1:8000>.

Use `POST /orders` in <http://127.0.0.1:8000/docs> to add test orders.

## Test

```bash
pytest
```
