# Traceability Matrix

| Story | Requirement | Endpoint Evidence | Test Evidence |
|---|---|---|---|
| US-01 | Manage sandwiches | `POST/GET/PUT/DELETE /sandwiches` | `test_sandwich_crud` |
| US-02 | Manage ingredient inventory | `POST/GET/PUT/DELETE /resources` | `test_related_table_crud_workflow` |
| US-03 | Configure recipes | `POST/GET/PUT/DELETE /recipes` | `test_related_table_crud_workflow` |
| US-04 | Manage orders and order items | CRUD under `/orders` and `/order_details` | `test_related_table_crud_workflow` |
| US-05 | Calculate totals and complete checkout | `GET /orders/{id}/summary`, `POST /orders/{id}/checkout` | Both checkout tests |

All five persistent tables expose create, read-all, read-one, update, and
delete operations. The checkout endpoint adds the final-project business rule:
an order can complete only once and only when every required resource is
available.
