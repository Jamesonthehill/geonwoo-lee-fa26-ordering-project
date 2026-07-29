# User Story #1: View Menu

This is a small FastAPI project for viewing a cafe menu.

It contains only:

- `main.py` — creates the menu table and provides the `/menu` endpoint
- `index.html` — displays names, prices, pictures, and availability
- `tests/test_main.py` — tests available and unavailable items

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
