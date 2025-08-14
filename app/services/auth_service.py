from app.db.database import get_db
from fastapi import Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.auth import verify_password
from datetime import datetime, timezone
from app.CRUD.session_operations import get_session
from app.CRUD.user_operations import get_user_by_username


async def authenticate_user(user_name: str, password: str, db: AsyncSession):
    user = await get_user_by_username(db, user_name=user_name)
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

    now_utc = datetime.now(timezone.utc)
    expires = session.expires_at

    if expires < now_utc:
        raise HTTPException(status_code=401, detail="Session expired")

    return session.user