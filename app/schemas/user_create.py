from pydantic import BaseModel
from app.core.enums import GenderEnum


class UserCreate(BaseModel):
    user_name: str
    password: str
    email: str

    first_name: str
    age: int
    gender: GenderEnum
