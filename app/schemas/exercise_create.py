from pydantic import BaseModel
from typing import Optional


class ExerciseCreate(BaseModel):
    name: str
    weight: Optional[float]
    sets: int
    reps: int
    description: Optional[str]