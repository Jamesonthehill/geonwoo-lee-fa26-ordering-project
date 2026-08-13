# User Story #9: Cancel an Order as Manager

This standalone FastAPI submission:

- displays confirmed and cancelled order statuses;
- lets a manager cancel a confirmed order;
- saves the cancelled status in SQLite;
- prevents an order from being cancelled twice;
- tests the complete manager cancellation flow.

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
