from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.CRUD.user_operations import add_user, get_user_by_username
from app.core.auth import get_password_hash
from app.models import User
from app.schemas.user_create import UserCreate


async def create_user(db: AsyncSession, user_data: UserCreate):
    existing_user = await get_user_by_username(db, user_data.user_name)

    if existing_user:
        raise HTTPException(status_code=400, detail="Пользователь с таким email или именем уже существует")

    hashed_password = get_password_hash(user_data.password)

    new_user = User(
        user_name=user_data.user_name,
        email=user_data.email,
        password=hashed_password,
        first_name=user_data.first_name,
        age=user_data.age,
        gender=user_data.gender
    )

    try:
        return await add_user(db, new_user)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Пользователь с таким email или именем уже существует")