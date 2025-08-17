from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import ForeignKey, text
from typing import Optional, TYPE_CHECKING
from app.db.database import Base

if TYPE_CHECKING:
    from .workout import Workout
    from .exercise_set import ExerciseSet


class Exercise(Base):
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[Optional[str]]

    workout_id: Mapped[int] = mapped_column(ForeignKey('workouts.id', ondelete='CASCADE'))
    workout: Mapped["Workout"] = relationship(
        "Workout",
        back_populates="exercises",
        passive_deletes=True,
    )
    sets: Mapped[list["ExerciseSet"]] = relationship(
        "ExerciseSet",
        back_populates="exercise",
        cascade="all, delete-orphan",
        order_by="ExerciseSet.position",
        passive_deletes=True
    )
