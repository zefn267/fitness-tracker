from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.CRUD.create_user import create_user
from app.CRUD.get_user import get_user
from app.db.database import get_db
from app.schemas.user_create import UserCreate
from app.schemas.user_info import UserInfo

router = APIRouter(prefix="/register", tags=["register"])

@router.post("/", response_model=UserInfo)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        new_user = await create_user(db, user)
    except Exception as err:
        raise HTTPException(status_code=400, detail=str(err))

    return new_user

@router.get("/user_id", response_model=UserInfo)
async def get_user_info(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user