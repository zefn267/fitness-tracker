from datetime import date
from typing import Optional
from pydantic import BaseModel


class WorkoutBase(BaseModel):
    name: str
    date: date
    workout_type: str
    description: Optional[str] = None
