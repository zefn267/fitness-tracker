import re
from pydantic import BaseModel, field_validator
from app.core.enums import GenderEnum


EMAIL_REGEX = re.compile(
    r"^(?=.{6,254}$)(?!.*\.\.)[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+"
    r"(?:\.[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+)*"
    r"@"
    r"(?:(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+"
    r"[A-Za-z]{2,63})$"
)


class UserCreate(BaseModel):
    user_name: str
    password: str
    email: str

    first_name: str
    age: int
    gender: GenderEnum

    @field_validator('email')
    def validate_email(cls, v: str):
        if not EMAIL_REGEX.match(v):
            raise ValueError('invalid email')
        return v

    @field_validator('age')
    def validate_first_name(cls, v: int):
        if v < 1 or v > 100:
            raise ValueError('age must be >= 1 and <= 100')
        return v
