from pydantic import BaseModel, ConfigDict
from typing import Optional


class Profile(BaseModel):
    first_name: str
    last_name: Optional[str]
    age: int
    gender: str

    model_config = ConfigDict(from_attributes=True)