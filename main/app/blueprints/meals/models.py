from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class MealItem(BaseModel):
    type: str
    calories: float
    protein: float
    carbs: float
    fat: float


class Meal(BaseModel):
    uuid: str
    date: datetime
    items: list[MealItem]
