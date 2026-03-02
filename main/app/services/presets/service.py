from app.extensions import get_db
from app.services.users.models import Activity
from .models import PresetWorkout

class PresetService:
    @staticmethod
    def get_preset_for_user(activity: Activity):
        db = get_db()

        activity_str = activity.value if hasattr(activity, 'value') else str(activity)

        data = db.presets.find_one({"target_activities": activity_str})
        if data:
            return PresetWorkout(**data)
        
        return None