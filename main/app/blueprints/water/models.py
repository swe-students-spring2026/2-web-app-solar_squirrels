from datetime import datetime
from pydantic import BaseModel


class WaterItem(BaseModel):
    time: datetime
    amount: int


class Water(BaseModel):
    user_id: str
    date: datetime
    water: list[WaterItem] = []