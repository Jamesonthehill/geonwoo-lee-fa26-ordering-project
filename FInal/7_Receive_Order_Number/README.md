# User Story #7: Receive an Order Number

This standalone FastAPI submission:

- generates a unique order number;
- returns the order number and confirmation from FastAPI;
- displays the confirmation on the customer page;
- tests all three requirements.

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
