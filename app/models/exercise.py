from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import ForeignKey
from typing import Optional, TYPE_CHECKING
from app.db.database import Base

if TYPE_CHECKING:
    from app.models.workout import Workout


class Exercise(Base):
    name: Mapped[str]
    weight: Mapped[Optional[float]]
    sets: Mapped[int]
    reps: Mapped[int]
    description: Mapped[Optional[str]]
    workout_id: Mapped[int] = mapped_column(ForeignKey('workouts.id'))
    workout: Mapped["Workout"] = relationship(
        "Workout",
        back_populates="exercises"
    )