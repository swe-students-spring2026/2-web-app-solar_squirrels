from app.blueprints.meals.models import Meal, MealEntry
from app.extensions import get_db
from datetime import datetime
from pymongo import ReturnDocument


class MealService:
    
    @staticmethod
    def get_user_meals(user_id: str, date: datetime) -> Meal:
        db = get_db()

        try:
            result = db.meals.find_one({"user_id": user_id, "date": date})
            if result:
                return Meal(**result)
            return Meal(user_id=user_id, date=date, meals=[])
        except Exception as e:
            raise Exception("Failed to get user meals")
    
    @staticmethod
    def update_meals(user_id: str, date: datetime, meal_entry: MealEntry) -> Meal:
        db = get_db()

        try:
            meal_entry_dict = meal_entry.model_dump()
            result = db.meals.find_one_and_update(
                {"user_id": user_id, "date": date},
                {
                    "$push": {"meals": meal_entry_dict},
                    "$setOnInsert": {"user_id": user_id, "date": date}
                },
                upsert=True,
                return_document=ReturnDocument.AFTER
            )
            return Meal(**result)
        except Exception as e:
            raise Exception("Failed to update meal: " + str(e))