from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User


async def add_user(db: AsyncSession, user: User):
    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user


async def get_user_by_username(db: AsyncSession, user_name: str):
    result = await db.execute(select(User).where(User.user_name == user_name))

    return result.scalar_one_or_none()