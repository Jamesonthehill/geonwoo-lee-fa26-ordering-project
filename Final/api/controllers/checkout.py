from collections import defaultdict

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ..models import models


def summarize(order):
    items = []
    total = 0.0

    for detail in order.order_details:
        unit_price = float(detail.sandwich.price)
        line_total = round(unit_price * detail.amount, 2)
        total += line_total
        items.append(
            {
                "order_detail_id": detail.id,
                "sandwich_id": detail.sandwich_id,
                "sandwich_name": detail.sandwich.sandwich_name,
                "quantity": detail.amount,
                "unit_price": unit_price,
                "line_total": line_total,
            }
        )

    return {
        "order_id": order.id,
        "customer_name": order.customer_name,
        "status": order.status,
        "total": round(total, 2),
        "items": items,
    }


def complete(db: Session, order):
    if order.status == "completed":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Order has already been checked out",
        )
    if not order.order_details:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Order must contain at least one sandwich",
        )

    required = defaultdict(int)
    resources = {}

    for detail in order.order_details:
        if not detail.sandwich.recipes:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"{detail.sandwich.sandwich_name} does not have a recipe",
            )
        for recipe in detail.sandwich.recipes:
            required[recipe.resource_id] += recipe.amount * detail.amount
            resources[recipe.resource_id] = recipe.resource

    shortages = [
        f"{resources[resource_id].item}: need {amount}, "
        f"have {resources[resource_id].amount}"
        for resource_id, amount in required.items()
        if resources[resource_id].amount < amount
    ]
    if shortages:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Insufficient resources - " + "; ".join(shortages),
        )

    for resource_id, amount in required.items():
        resources[resource_id].amount -= amount

    order.status = "completed"
    db.commit()
    db.refresh(order)
    return summarize(order)
