from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class Set(BaseModel):
    reps: int
    weight: Optional[float] = None


class WorkoutDetail(BaseModel):
    type: str
    duration: int
    sets: Optional[List[Set]] = None
    calories: Optional[float] = None


class Workout(BaseModel):
    workout_uuid: str
    user_uuid: str
    date: datetime
    workout: WorkoutDetail