from pydantic import BaseModel, ConfigDict
from app.schemas.exercise_info import ExerciseInfo
from typing import Optional, List
from datetime import date

class WorkoutInfo(BaseModel):
    id: int
    date: date
    exercises: Optional[List[ExerciseInfo]]
    description: Optional[str]

    model_config = ConfigDict(from_attributes=True)
