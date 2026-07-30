# User Story #3: Customize the Item

This standalone FastAPI submission:

- adds small, medium, and large size options;
- adds controls for adding or removing ingredients;
- recalculates the item price after customization;
- tests customization and price calculations.

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
