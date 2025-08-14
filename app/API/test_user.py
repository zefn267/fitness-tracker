from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.user_service import create_user
from app.services.auth_service import get_current_user
from app.db.database import get_db
from app.schemas.user_create import UserCreate
from app.schemas.user_info import UserInfo


router = APIRouter(prefix="", tags=["register"])

@router.post("/register", response_model=UserInfo)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        new_user = await create_user(db, user)
    except Exception as err:
        raise HTTPException(status_code=400, detail=str(err))

    return new_user

@router.get("/profile", response_model=UserInfo)
async def get_user_info(current_user = Depends(get_current_user)):
    return current_user