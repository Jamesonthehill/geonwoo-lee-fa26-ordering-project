# User Stories #1 and #2: View and Select Menu Items

This small FastAPI project lets a customer view a cafe menu, select an
available item, and choose a quantity from 1 to 10.

It contains only:

- `main.py` — menu and item-selection endpoints
- `index.html` — menu, Select Item buttons, quantity, and order form
- `tests/test_main.py` — menu, selection, and quantity tests

## Run the project

Create and activate a virtual environment, then install the dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Start the app:

```bash
uvicorn main:app --reload
```

Open <http://127.0.0.1:8000> for the customer menu or
<http://127.0.0.1:8000/docs> for the interactive API documentation.

The app automatically creates `menu.db` with three sample items.

The menu API is available at <http://127.0.0.1:8000/menu>.

To run the tests:

```bash
pytest
```
