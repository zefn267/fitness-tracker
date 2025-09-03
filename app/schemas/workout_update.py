from typing import Optional
from pydantic import BaseModel, field_validator
from datetime import date as Date


class WorkoutUpdate(BaseModel):
    date: Optional[Date] = None
    name: Optional[str] = None
    workout_type: Optional[str] = None
    description: Optional[str] = None

    @field_validator('date', mode='before')
    def validate_date(cls, v):
        if v is None:
            raise ValueError('date must not be None')
        return v
