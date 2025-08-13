from datetime import datetime, timezone

from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from app.CRUD.get_user import get_user
from fastapi import Request, HTTPException, Depends
from app.CRUD.session_operations import get_session
from app.db.database import get_db


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def authenticate_user(user_name: str, password: str, db: AsyncSession):
    user = await get_user(db, user_name=user_name)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False

    return user


async def get_current_user(request: Request, db: AsyncSession = Depends(get_db)):
    session_id = request.cookies.get('session_id')
    if not session_id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    session = await get_session(db, session_id=session_id)
    if not session:
        raise HTTPException(status_code=401, detail="Session not found")

    if session.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=401, detail="Session expired")

    return session.user
