from app.blueprints.meals.models import Meal
from app.extensions import get_db
from datetime import datetime


class MealService:
    
    @staticmethod
    def get_user_meals(uuid: str, date: datetime) -> list[Meal]:
        db = get_db()

        try:
            result = db.meals.find({"user_id": uuid, "date": date})
            return [Meal(**meal) for meal in result]
        except Exception as e:
            raise Exception("Failed to get user meals")
    
    @staticmethod
    def update_meals(uuid: str, date: datetime, meal: Meal) -> Meal:
        db = get_db()

        try:
            meal_dict = meal.model_dump()
            result = db.meals.update_one(
                {"uuid": uuid, "date": date},
                {"$set": meal_dict},
                upsert=True
            )
            return meal
        except Exception as e:
            raise Exception("Failed to update meal")