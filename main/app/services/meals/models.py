from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class MealItem(BaseModel):
    type: str
    calories: float
    protein: float
    carbs: float
    fat: float


class MealEntry(BaseModel):
    items: list[MealItem]


class Meal(BaseModel):
    user_id: str
    date: datetime
    meals: list[MealEntry] = []
