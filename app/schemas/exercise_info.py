from typing import Optional
from pydantic import BaseModel, ConfigDict


class ExerciseInfo(BaseModel):
    id: int
    name: str
    weight: Optional[float]
    sets: int
    reps: int
    description: Optional[str]

    model_config = ConfigDict(from_attributes=True)