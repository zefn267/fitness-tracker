from pydantic import BaseModel, ConfigDict
from app.core.enums import GenderEnum


class UserInfo(BaseModel):
    id: int
    user_name: str
    email: str

    first_name: str
    age: int
    gender: GenderEnum

    model_config = ConfigDict(from_attributes=True)
