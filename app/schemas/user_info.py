from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from app.schemas.profile import Profile

class UserInfo(BaseModel):
    id: int
    user_name:str
    email: EmailStr
    profile: Optional[Profile]

    model_config = ConfigDict(from_attributes=True)
