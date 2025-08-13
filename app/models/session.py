from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base
from datetime import datetime


if TYPE_CHECKING:
    from app.models.user import User


class Session(Base):
    session_id: Mapped[str] = mapped_column(unique=True)
    expires_at: Mapped[datetime]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(
        "User",
        back_populates="sessions"
    )
