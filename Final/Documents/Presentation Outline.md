# 4-5 Minute Presentation Outline

## 0:00-0:40 - Introduction

Introduce the Sandwich Shop Ordering API. Explain that it manages the menu,
ingredients, recipes, orders, and order items while preventing checkout when
inventory is insufficient.

## 0:40-1:20 - Architecture

Show the FastAPI project folders. Briefly identify routes, controllers,
Pydantic schemas, SQLAlchemy models, MySQL, and pytest.

## 1:20-3:30 - Live Demo

1. Open Swagger and run `GET /health`.
2. Show the sample sandwich, resources, and recipe.
3. Show a pending order and its calculated summary.
4. Execute checkout.
5. Show the completed status and order total.
6. Show that resource quantities decreased.
7. Attempt checkout again and show the controlled `409` response.

## 3:30-4:15 - Testing

Run `python -m pytest -q`. Explain that the tests cover CRUD, successful
checkout, inventory deduction, duplicate checkout, and insufficient inventory.

## 4:15-5:00 - Challenges And Learning

Discuss database relationships, preventing partial inventory updates, keeping
tests independent from MySQL, and tracing user stories to endpoints and tests.
