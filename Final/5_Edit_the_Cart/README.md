# User Story #5: Edit the Cart

This standalone FastAPI submission:

- changes item quantities;
- removes items from the cart;
- recalculates line totals and the cart subtotal;
- tests cart editing and the complete order-submission flow.

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
