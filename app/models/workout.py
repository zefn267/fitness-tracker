from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column
from typing import Optional, TYPE_CHECKING
from app.db.database import Base
from datetime import date


if TYPE_CHECKING:
    from app.models.exercise import Exercise
    from app.models.user import User


class Workout(Base):
    name: Mapped[str]
    date: Mapped[date]
    workout_type: Mapped[str]
    description: Mapped[Optional[str]]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    exercises: Mapped[list["Exercise"]] = relationship(
        "Exercise",
        back_populates="workout",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
    user: Mapped["User"] = relationship(
        "User",
        back_populates="workouts",
    )