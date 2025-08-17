import enum
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base
from app.core.enums import GenderEnum

if TYPE_CHECKING:
    from app.models.session import Session
    from app.models.workout import Workout


class User(Base):
    user_name: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]

    first_name: Mapped[str]
    age: Mapped[int]
    gender: Mapped[GenderEnum]

    sessions: Mapped[list['Session']] = relationship(
        'Session',
        back_populates='user'
    )
    workouts: Mapped[list['Workout']] = relationship(
        'Workout',
        back_populates='user'
    )
