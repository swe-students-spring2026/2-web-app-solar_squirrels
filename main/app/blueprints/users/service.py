import uuid as uuid_lib
from datetime import datetime, timezone
from pymongo import ReturnDocument
from app.extensions import get_db
from app.blueprints.users.models import (
    UserCreate,
    UserUpdate,
    User,
)


class UserService:

    @staticmethod
    def get_all_users():
        db = get_db()
        users = db.users.find({})
        return [
            User(**user).model_dump(mode="json")
            for user in users
        ]

    @staticmethod
    def get_user_by_uuid(uuid: str):
        db = get_db()
        user = db.users.find_one({"uuid": uuid})
        if not user:
            return None

        return User(**user).model_dump(mode="json")

    # Specifically for user creation flow, only username required at creation time
    @staticmethod
    def create_user(user_data: dict):
        db = get_db()

        validated = UserCreate(**user_data)

        now = datetime.now(timezone.utc)

        user_dict = {
            "uuid": str(uuid_lib.uuid4()),
            "username": validated.username,
            "created_at": now,
            "updated_at": now,
        }

        db.users.insert_one(user_dict)

        return User(**user_dict).model_dump(mode="json")

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

        return User(**result).model_dump(mode="json")

    @staticmethod
    def delete_user(uuid: str):
        db = get_db()
        result = db.users.delete_one({"uuid": uuid})
        return result.deleted_count > 0