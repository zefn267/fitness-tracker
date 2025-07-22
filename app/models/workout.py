from sqlalchemy.orm import Mapped, relationship
from typing import Optional, TYPE_CHECKING
from app.db.database import Base
from datetime import date


if TYPE_CHECKING:
    from app.models.exercise import Exercise


class Workout(Base):
    date: Mapped[date]
    description: Mapped[Optional[str]]
    exercises: Mapped["Exercise"] = relationship(
        "Exercise",
        back_populates="workout",
        cascade="all, delete-orphan",
    )