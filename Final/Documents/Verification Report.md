# Verification Report

## Automated Tests

Command:

```bash
python -m pytest -q
```

Result:

```text
4 passed
```

The tests verify:

- Sandwich create, read, update, and delete
- CRUD across resources, recipes, orders, and order details
- Order total calculation
- Successful inventory deduction
- Rejection of insufficient inventory
- Rejection of repeated checkout

## OpenAPI Verification

- 14 paths
- 29 HTTP operations
- CRUD groups for all five persistent tables
- Additional System and Checkout groups

## Artifact Verification

- Product Backlog workbook rendered and inspected
- User Stories workbook rendered and inspected
- Both Sprint Backlog sheets rendered and inspected
- Formula scans found no spreadsheet errors
- Sprint Review 1 rendered across two pages
- Sprint Review 2 rendered across two pages
- No clipping, overlap, or missing content was found

## MySQL Note

The final project expects a fresh MySQL database named
`sandwich_shop_final`. SQLAlchemy creates the five tables when the API starts.
Automated tests use an isolated SQLite database so they do not change MySQL
presentation data.
