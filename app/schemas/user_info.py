from pydantic import BaseModel, EmailStr
from typing import Optional
from app.schemas.profile import Profile

class UserInfo(BaseModel):
    id: int
    user_name:str
    email: EmailStr
    profile: Optional[Profile]

    class Config:
        orm_mode = True
