from pydantic import BaseModel
from typing import Optional, List
from datetime import date


class WorkoutCreate(BaseModel):
    date: date
    description: Optional[str]