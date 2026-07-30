from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel


app = FastAPI(title="Customize an Item")

BASE_PRICE = 8.00
SIZE_PRICES = {"small": 0.00, "medium": 1.50, "large": 3.00}
INGREDIENT_PRICES = {"cheese": 1.00, "bacon": 1.50, "avocado": 2.00}


class Customization(BaseModel):
    size: str
    ingredients: list[str]


@app.get("/")
def customization_page():
    return FileResponse("index.html")


@app.post("/customize")
def customize_item(customization: Customization):
    if customization.size not in SIZE_PRICES:
        raise HTTPException(status_code=400, detail="Invalid size")

    invalid_ingredients = set(customization.ingredients) - set(INGREDIENT_PRICES)
    if invalid_ingredients:
        raise HTTPException(status_code=400, detail="Invalid ingredient")

    price = BASE_PRICE + SIZE_PRICES[customization.size]
    price += sum(
        INGREDIENT_PRICES[ingredient]
        for ingredient in customization.ingredients
    )

    return {
        "item": "Breakfast Sandwich",
        "size": customization.size,
        "ingredients": customization.ingredients,
        "price": round(price, 2),
    }
