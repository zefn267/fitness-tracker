from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User

async def get_user(db: AsyncSession, username: str):
    result = await db.execute(select(User).where(User.user_name == username))

    return result.scalar_one_or_none()