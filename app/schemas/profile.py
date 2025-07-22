from pydantic import BaseModel
from typing import Optional


class Profile(BaseModel):
    first_name: str
    last_name: Optional[str]
    age: int
    gender: str

    class Config:
        orm_mode = True