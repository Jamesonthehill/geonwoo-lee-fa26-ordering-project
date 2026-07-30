# User Story #4: Add the Item to the Cart

This standalone FastAPI submission:

- creates a cart data structure;
- adds the selected item, quantity, and price;
- displays cart contents and the subtotal;
- tests adding items to the cart.

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
