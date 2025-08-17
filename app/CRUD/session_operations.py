import uuid
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.session import Session
from datetime import datetime, timezone, timedelta


async def create_session(db: AsyncSession, user_id: int, ttl_hours: int = 24):
    session_id = str(uuid.uuid4())
    expires_at = datetime.now(timezone.utc) + timedelta(hours=ttl_hours)

    session = Session(session_id=session_id, expires_at=expires_at, user_id=user_id)

    db.add(session)

    await db.commit()
    await db.refresh(session)

    return session


async def get_session(db: AsyncSession, session_id: str):
    result = await db.execute(select(Session).options(selectinload(Session.user)).where(Session.session_id == session_id))

    return result.scalar_one_or_none()


async def delete_session(db: AsyncSession, session_id: str):
    await db.execute(delete(Session).where(Session.session_id == session_id))
    await db.commit()

    return True
