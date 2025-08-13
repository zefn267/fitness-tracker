from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.auth import get_password_hash
from app.models.user import User
from app.schemas.user_create import UserCreate


async def create_user(db: AsyncSession, user_data: UserCreate):
    existing_user = await db.execute(
        select(User)
        .where(
            (User.email == user_data.email) | (User.user_name == user_data.user_name)
        )
    )

    if existing_user.scalar():
        raise HTTPException(status_code=400, detail="Пользователь с таким email или именем уже существует.")

    hashed_password = get_password_hash(user_data.password)

    new_user = User(
        user_name=user_data.user_name,
        email=user_data.email,
        password=hashed_password,
        first_name=user_data.first_name,
        age=user_data.age,
        gender=user_data.gender
    )

    db.add(new_user)

    await db.commit()
    await db.refresh(new_user)

    return new_user
