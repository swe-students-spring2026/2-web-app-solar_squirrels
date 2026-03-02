import uuid as uuid_lib
from datetime import datetime, timezone
from app.extensions import get_db
from app.services.workouts.models import Workout


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
    def update_workout(user_uuid: str, workout_uuid: str, update_data: dict):
        db = get_db()

        existing_workout_doc = db.workouts.find_one({
            "user_uuid": user_uuid,
            "workout_uuid": workout_uuid
        })

        if not existing_workout_doc:
            return None

        date_str = update_data.get("date")
        if date_str:
            try:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            except ValueError:
                date_obj = existing_workout_doc.get("date")
        else:
            date_obj = existing_workout_doc.get("date")

        raw_reps = update_data.get("reps")
        raw_weight = update_data.get("weight")
        current_detail = existing_workout_doc.get("workout", {})
        
        updated_detail = {
            "type": update_data.get("type", current_detail.get("type")),
            "duration": int(update_data["duration"]) if update_data.get("duration") and str(update_data["duration"]).strip() != "" else current_detail.get("duration"),
            "calories": float(update_data["calories"]) if update_data.get("calories") and str(update_data["calories"]).strip() != "" else current_detail.get("calories"),
        }

        if raw_reps is not None and str(raw_reps).strip() != "":
            updated_detail["sets"] = [{
                "reps": int(raw_reps),
                "weight": float(raw_weight) if raw_weight and str(raw_weight).strip() != "" else None
            }]
        else:
            updated_detail["sets"] = current_detail.get("sets")

        workout_payload = {
            "workout_uuid": workout_uuid,
            "user_uuid": user_uuid,
            "date": date_obj,
            "workout": updated_detail
        }
        print(workout_payload)
        
        validated_workout = Workout(**workout_payload)

        db.workouts.update_one(
            {"workout_uuid": workout_uuid, "user_uuid": user_uuid},
            {"$set": validated_workout.model_dump()}
        )

        return validated_workout.model_dump(mode="json")
    
    @staticmethod
    def delete_workout(user_uuid: str, workout_uuid: str):
        db = get_db()

        result = db.workouts.delete_one({
            "user_uuid": user_uuid,
            "workout_uuid": workout_uuid
        })

        return result.deleted_count > 0

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