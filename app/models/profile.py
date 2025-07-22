from typing import Optional, TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base
import enum


if TYPE_CHECKING:
    from app.models.user import User


class GenderEnum(str, enum.Enum):
    MALE = "Мужской"
    FEMALE = "Женский"


class Profile(Base):
    first_name: Mapped[str]
    last_name: Mapped[Optional[str]]
    age: Mapped[int]
    gender: Mapped[GenderEnum]
    user: Mapped["User"] = relationship(
        "User",
        back_populates="profile",
        uselist=False
    )
