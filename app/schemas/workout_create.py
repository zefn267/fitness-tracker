from pydantic import BaseModel
from typing import Optional, List
from datetime import date

from app.schemas.exercise_info import ExerciseInfo


class WorkoutCreate(BaseModel):
    name: str
    date: date
    workout_type: str
    description: Optional[str]
    exercises: Optional[List[ExerciseInfo]]