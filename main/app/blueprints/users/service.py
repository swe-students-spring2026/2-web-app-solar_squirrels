from app.extensions import get_db
from datetime import datetime, timezone
from pymongo import ReturnDocument


class UserService:

    @staticmethod
    def get_all_users():
        db = get_db()
        users = list(db.users.find({}))
        for user in users:
            user['_id'] = str(user['_id'])
        return users

    @staticmethod
    def get_user_by_uuid(uuid):
        db = get_db()
        try:
            user = db.users.find_one({'uuid': uuid})
            if user:
                user['_id'] = str(user['_id'])
            return user
        except Exception:
            return None

    @staticmethod
    def create_user(user_data):
        db = get_db()
        now = datetime.now(timezone.utc)

        user_data['created_at'] = now
        user_data['updated_at'] = now

        result = db.users.insert_one(user_data)
        user_data['_id'] = str(result.inserted_id)
        return user_data

    @staticmethod
    def update_user(uuid, update_data):
        db = get_db()
        try:
            update_data['updated_at'] = datetime.now(timezone.utc)

            result = db.users.find_one_and_update(
                {'uuid': uuid},
                {'$set': update_data},
                return_document=ReturnDocument.AFTER
            )

            if result:
                result['_id'] = str(result['_id'])

            return result
        except Exception:
            return None

    @staticmethod
    def delete_user(uuid):
        db = get_db()
        try:
            result = db.users.delete_one({'uuid': uuid})
            return result.deleted_count > 0
        except Exception:
            return False