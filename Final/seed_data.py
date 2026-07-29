from api.dependencies.database import SessionLocal
from api.models import models


def seed():
    db = SessionLocal()
    try:
        if db.query(models.Sandwich).first():
            print("Sample data already exists; no changes made.")
            return

        bread = models.Resource(item="bread", amount=40)
        ham = models.Resource(item="ham", amount=30)
        cheese = models.Resource(item="cheese", amount=30)
        sandwich = models.Sandwich(sandwich_name="Ham Sandwich", price=5.99)
        db.add_all([bread, ham, cheese, sandwich])
        db.flush()

        db.add_all(
            [
                models.Recipe(
                    sandwich_id=sandwich.id,
                    resource_id=bread.id,
                    amount=2,
                ),
                models.Recipe(
                    sandwich_id=sandwich.id,
                    resource_id=ham.id,
                    amount=4,
                ),
                models.Recipe(
                    sandwich_id=sandwich.id,
                    resource_id=cheese.id,
                    amount=2,
                ),
            ]
        )
        order = models.Order(
            customer_name="Sample Customer",
            description="Presentation order",
        )
        db.add(order)
        db.flush()
        db.add(
            models.OrderDetail(
                order_id=order.id,
                sandwich_id=sandwich.id,
                amount=2,
            )
        )
        db.commit()
        print("Sample sandwich, resources, recipe, and pending order created.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
