from pydantic import ConfigDict
from app.schemas.exercise_info import ExerciseInfo
from typing import Optional, List
from app.schemas.workout_base import WorkoutBase


class WorkoutInfo(WorkoutBase):
    id: int
    exercises: Optional[List[ExerciseInfo]] = None

    model_config = ConfigDict(from_attributes=True)
