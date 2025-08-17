from typing import Optional
from pydantic import BaseModel, ConfigDict
from app.schemas.exercise_set_in import ExerciseSetIn


class ExerciseInfo(BaseModel):
    id: int
    name: str
    workout_id: int
    description: Optional[str]
    sets: list[ExerciseSetIn]

    model_config = ConfigDict(from_attributes=True)