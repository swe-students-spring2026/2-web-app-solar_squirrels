from app.blueprints.water.models import Water, WaterItem
from app.extensions import get_db
from datetime import datetime
from pymongo import ReturnDocument


class WaterService:
    
    @staticmethod
    def get_user_water(user_id: str, date: datetime) -> Water:
        db = get_db()

        try:
            result = db.water.find_one({"user_id": user_id, "date": date})
            if result:
                return Water(**result)
            return Water(user_id=user_id, date=date, water=[])
        except Exception as e:
            raise Exception("Failed to get user water")

    @staticmethod
    def update_water(user_id: str, date: datetime, water_item: WaterItem) -> Water:
        db = get_db()

        try:
            water_item_dict = water_item.model_dump()
            result = db.water.find_one_and_update(
                {"user_id": user_id, "date": date},
                {
                    "$push": {"water": water_item_dict},
                    "$setOnInsert": {"user_id": user_id, "date": date}
                },
                upsert=True,
                return_document=ReturnDocument.AFTER
            )
            return Water(**result)
        except Exception as e:
            raise Exception("Failed to update water: " + str(e))
