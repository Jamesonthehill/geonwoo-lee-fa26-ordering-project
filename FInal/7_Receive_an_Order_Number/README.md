# User Story #7: Receive an Order Number

This folder is a standalone FastAPI submission for order confirmation.

- `main.py` generates a unique order number and returns it from FastAPI.
- `index.html` displays the confirmation and order number.
- `tests/test_main.py` tests unique numbers, the API response, and the page.

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
