from pydantic import BaseModel
from typing import Optional


class ExerciseCreate(BaseModel):
    name: str
    weight: Optional[float]
    approaches: int
    times: int
    description: Optional[str]