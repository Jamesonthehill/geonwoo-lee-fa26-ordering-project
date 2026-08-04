# User Story #8: View Customer Orders

This standalone FastAPI submission:

- provides a manager endpoint for retrieving customer orders;
- returns order numbers, items, quantities, and totals;
- displays the orders in a manager history table;
- includes two sample customer orders for testing.

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
