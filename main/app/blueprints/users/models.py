from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class Activity(str, Enum):
    sedentary = "sedentary"
    lightly_active = "lightly_active"
    active = "active"
    very_active = "very_active"


class Goal(str, Enum):
    lose_weight = "lose_weight"
    maintain_weight = "maintain_weight"
    gain_weight = "gain_weight"

class UserCreate(BaseModel):
    username: str

class UserUpdate(BaseModel):
    age: int
    height: int
    weight: int
    activity: Activity
    goals: Goal

class User(BaseModel):
    uuid: str
    username: str

    age: Optional[int] = None
    height: Optional[int] = None
    weight: Optional[int] = None
    activity: Optional[Activity] = None
    goals: Optional[Goal] = None

    created_at: datetime
    updated_at: datetime