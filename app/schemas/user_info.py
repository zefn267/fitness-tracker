from pydantic import BaseModel, EmailStr, ConfigDict


class UserInfo(BaseModel):
    id: int
    user_name: str
    email: EmailStr

    first_name: str
    age: int
    gender: str

    model_config = ConfigDict(from_attributes=True)
