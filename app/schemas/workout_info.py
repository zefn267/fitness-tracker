from pydantic import BaseModel
from app.schemas.exercise_info import ExerciseInfo
from typing import Optional, List
from datetime import date

class WorkoutInfo(BaseModel):
    id: int
    date: date
    exercises: List[ExerciseInfo]
    description: Optional[str]

    class Config:
        orm_mode = True
