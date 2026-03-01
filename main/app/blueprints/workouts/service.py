import uuid as uuid_lib
from datetime import datetime, timezone
from app.extensions import get_db
from app.blueprints.workouts.models import Workout


class WorkoutService:

    @staticmethod
    def create_workout(user_uuid: str, workout_data: dict):
        db = get_db()

        now = datetime.now(timezone.utc)

        workout_dict = {
            "workout_uuid": str(uuid_lib.uuid4()),
            "user_uuid": user_uuid,
            "date": workout_data.get("date", now),
            "workout": workout_data["workout"],
        }

        validated = Workout(**workout_dict)

        db.workouts.insert_one(validated.model_dump())

        return validated.model_dump(mode="json")


    @staticmethod
    def get_workouts_by_user(user_uuid: str):
        db = get_db()

        workouts = db.workouts.find(
            {"user_uuid": user_uuid}
        ).sort("date", -1)

        return [
            Workout(**workout).model_dump(mode="json")
            for workout in workouts
        ]


    @staticmethod
    def get_workout_by_uuid(user_uuid: str, workout_uuid: str):
        db = get_db()

        workout = db.workouts.find_one({
            "user_uuid": user_uuid,
            "workout_uuid": workout_uuid
        })

        if not workout:
            return None

        return Workout(**workout).model_dump(mode="json")