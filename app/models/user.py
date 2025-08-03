from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base
from app.models.profile import Profile


class User(Base):
    user_name: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    profile_id: Mapped[Optional[int]] = mapped_column(ForeignKey("profiles.id"))
    profile: Mapped[Optional[Profile]] = relationship(
        Profile,
        back_populates="user",
        uselist=False,
        lazy="joined"
    )

