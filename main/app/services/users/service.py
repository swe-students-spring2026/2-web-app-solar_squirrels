import uuid as uuid_lib
from datetime import datetime, timezone
from pymongo import ReturnDocument
from app.extensions import get_db
from werkzeug.security import generate_password_hash, check_password_hash
from app.services.users.models import (
    UserCreate,
    UserUpdate,
    User,
)


class UserService:

    @staticmethod
    def get_all_users():
        db = get_db()
        users = db.users.find({})
        return [User(**user) for user in users]

    @staticmethod
    def get_user_by_uuid(uuid: str):
        db = get_db()
        user = db.users.find_one({"uuid": uuid})
        if not user:
            return None

        return User(**user)
    
    @staticmethod
    def get_tdee_for_user(uuid: str):
        db = get_db()
        user = db.users.find_one({"uuid": uuid})
        if not user:
            return None

        weight = user.get("weight")
        height = user.get("height")
        age = user.get("age")
        activity = user.get("activity")

        if not all([weight, height, age, activity]):
            return None
        
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 78

        activity_levels = {
            "sedentary": 1.2,
            "lightly_active": 1.4,
            "active": 1.7,
            "very_active": 2.0,
        }

        multiplier = activity_levels.get(activity, 1.2)
        tdee = bmr * multiplier

        return round(tdee)


    # Step 2 of user creation flow, update with personal details
    @staticmethod
    def update_user(uuid: str, update_data: dict):
        db = get_db()

        existing = db.users.find_one({"uuid": uuid})
        if not existing:
            return None

        validated = UserUpdate(**update_data)

        update_dict = validated.model_dump()
        update_dict["updated_at"] = datetime.now(timezone.utc)

        result = db.users.find_one_and_update(
            {"uuid": uuid},
            {"$set": update_dict},
            return_document=ReturnDocument.AFTER
        )

        return User(**result)

    @staticmethod
    def delete_user(uuid: str):
        db = get_db()
        result = db.users.delete_one({"uuid": uuid})
        return result.deleted_count > 0
    
    @staticmethod
    def create_user(user_data: dict):
        db = get_db()
        
        validated = UserCreate(**user_data)

        hashed_pw = generate_password_hash(validated.password)
        now = datetime.now(timezone.utc)
        user_dict = {
            "uuid": str(uuid_lib.uuid4()),
            "username": validated.username,
            "password_hash": hashed_pw,
            "created_at": now,
            "updated_at": now,
            "age": None,
            "height": None,
            "weight": None,
            "activity": None,
            "goals": None
        }
        
        db.users.insert_one(user_dict)
        return User(**user_dict)

    @staticmethod
    def authenticate_user(username, password):
        db = get_db()
        user = db.users.find_one({"username": username})
        
        if user and check_password_hash(user.get("password_hash"), password):
            return user
        return None