from fastapi import APIRouter, Depends, HTTPException
from app.services.auth_service import get_current_user
from app.schemas.user_info import UserInfo


user_router = APIRouter(prefix='/api/user', tags=['user'])


@user_router.get("/profile", response_model=UserInfo)
async def get_user_info(current_user = Depends(get_current_user)):
    return current_user