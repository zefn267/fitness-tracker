import enum
from sqlalchemy.orm import Mapped, mapped_column
from app.db.database import Base


class GenderEnum(str, enum.Enum):
    MALE = "Мужской"
    FEMALE = "Женский"


class User(Base):
    user_name: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]

    first_name: Mapped[str]
    age: Mapped[int]
    gender: Mapped[GenderEnum]
