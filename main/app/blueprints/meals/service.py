from app.blueprints.meals.models import Meal
from app.extensions import get_db


class MealService:
    
    @staticmethod
    def get_user_meals(uuid: str, date: datetime) -> list[Meal]:
        db = get_db()

        try:
            result = db.meals.find({"user_id": uuid, "date": date})
            return [Meal(**meal) for meal in result]
        except Exception as e:
            raise Exception("Failed to get user meals")