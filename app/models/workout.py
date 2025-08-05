from sqlalchemy.orm import Mapped, relationship
from typing import Optional, TYPE_CHECKING, List
from app.db.database import Base
from datetime import date


if TYPE_CHECKING:
    from app.models.exercise import Exercise


class Workout(Base):
    date: Mapped[date]
    description: Mapped[Optional[str]]
    exercises: Mapped[List["Exercise"]] = relationship(
        "Exercise",
        back_populates="workout",
        cascade="all, delete-orphan",
        lazy="select"
    )