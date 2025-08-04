import enum
from pydantic import BaseModel


class GenderEnum(str, enum.Enum):
    MALE = "Мужской"
    FEMALE = "Женский"


class UserCreate(BaseModel):
    user_name: str
    password: str
    email: str

    first_name: str
    age: int
    gender: GenderEnum