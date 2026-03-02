import uuid as uuid_lib
from datetime import datetime, timezone
from app.extensions import get_db
from app.blueprints.workouts.models import Workout


class WorkoutService:
    @staticmethod
    def create_workout(user_uuid: str, workout_data: dict):
        db = get_db()
        
        date_obj = datetime.now(timezone.utc)

        raw_reps = workout_data.get("reps")
        raw_weight = workout_data.get("weight")
        raw_duration = workout_data.get("duration")
        raw_calories = workout_data.get("calories")
        
        sets_list = []
        if raw_reps is not None and str(raw_reps).strip() != "":
            sets_list.append({
                "reps": int(raw_reps),
                "weight": float(raw_weight) if raw_weight and str(raw_weight).strip() != "" else None
            })

        workout_payload = {
            "workout_uuid": str(uuid_lib.uuid4()),
            "user_uuid": user_uuid,
            "date": date_obj,
            "workout": {
                "type": workout_data.get("type", "General"),
                "duration": int(raw_duration) if raw_duration and str(raw_duration).strip() != "" else 0,
                "calories": float(raw_calories) if raw_calories and str(raw_calories).strip() != "" else None,
                "sets": sets_list if sets_list else None
            }
        }

        validated_workout = Workout(**workout_payload)
        db.workouts.insert_one(validated_workout.model_dump())

        return validated_workout.model_dump(mode="json")


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