from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class Exercise(BaseModel):
    name: str
    sets: int
    reps: int

class WorkoutGroup(BaseModel):
    name: str
    exercises: List[Exercise]

class PresetWorkout(BaseModel):
    level: str
    description: str
    target_activities: List[str]
    groups: List[WorkoutGroup]