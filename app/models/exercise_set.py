from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import ForeignKey, text, UniqueConstraint, CheckConstraint, Index
from typing import TYPE_CHECKING
from app.db.database import Base


if TYPE_CHECKING:
    from .exercise import Exercise


class ExerciseSet(Base):
    position: Mapped[int] = mapped_column(nullable=False)
    reps: Mapped[int] = mapped_column(nullable=False)
    rpe: Mapped[int] = mapped_column(nullable=False)
    rest_seconds: Mapped[int] = mapped_column(nullable=False)
    weight: Mapped[float] = mapped_column(default=0, server_default=text('0'))

    exercise_id: Mapped[int] = mapped_column(ForeignKey('exercises.id', ondelete="CASCADE"))
    exercise: Mapped["Exercise"] = relationship("Exercise", back_populates="sets")

    __table_args__ = (
        UniqueConstraint('exercise_id', 'position', name='uq_exercise_set_position'),
        CheckConstraint('reps >= 0', name='ck_exercise_set_reps_not_negative'),
        CheckConstraint('rest_seconds >= 0', name='ck_exercise_set_rest_not_negative'),
        CheckConstraint('(rpe BETWEEN 1 AND 10)', name='ck_exercise_set_rpe_range'),
        CheckConstraint('weight >= 0', name='ck_exercise_set_weight_not_negative'),
    )
