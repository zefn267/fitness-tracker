from fastapi import Depends, APIRouter, Request, Response, HTTPException, Form
from app.core.auth import get_current_user, authenticate_user
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.CRUD.session_operations import create_session, delete_session


router = APIRouter(tags=["user"])


@router.post("/login")
async def login(res: Response, username: str = Form(), password: str = Form(), db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(username, password, db)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    session = await create_session(db, user_id=user.id)

    res.set_cookie(
        key="session_id",
        value=session.session_id,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=24*3600
    )

    return {"message": "success"}


@router.post("/logout")
async def logout(req: Request, res: Response, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    session_id = req.cookies.get("session_id")
    if not session_id:
        raise HTTPException(status_code=401, detail="No session cookie found")

    await delete_session(db, session_id)

    res.delete_cookie("session_id")

    return {"message": "Logged out"}

