from pydantic import BaseModel, EmailStr


class UserRegister(BaseModel):
    user_name: str
    password: str
    email: EmailStr