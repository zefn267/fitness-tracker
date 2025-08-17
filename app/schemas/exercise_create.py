from pydantic import BaseModel, field_validator
from typing import Optional

from app.schemas.exercise_set_in import ExerciseSetIn


class ExerciseCreate(BaseModel):
    name: str
    description: Optional[str]
    workout_id: int
    sets: list[ExerciseSetIn]

    @field_validator('sets')
    def validate_sets(cls, v: list[ExerciseSetIn]):
        if not v:
            raise ValueError('sets must not be empty')

        positions = sorted(s.position for s in v)
        if positions != list(range(1, len(v) + 1)):
            raise ValueError('positions must contain 1..N')

        return v
