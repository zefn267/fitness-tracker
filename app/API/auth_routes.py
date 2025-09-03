from fastapi import Depends, APIRouter, Request, Response, HTTPException, Form, status
from app.schemas.user_create import UserCreate
from app.schemas.user_info import UserInfo
from app.services.auth_service import get_current_user, authenticate_user
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.CRUD.session_operations import create_session, delete_session
from app.services.user_service import create_user


auth_router = APIRouter(prefix='/api/auth', tags=['auth'])


@auth_router.post('/register', response_model=UserInfo, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        new_user = await create_user(db, user)
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))

    return new_user


@auth_router.post('/login', status_code=status.HTTP_200_OK)
async def login(res: Response, username: str = Form(), password: str = Form(), db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(username, password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect username or password')

    session = await create_session(db, user_id=user.id)

    res.set_cookie(
        key='session_id',
        value=session.session_id,
        httponly=True,
        secure=False,
        samesite='lax',
        max_age=24*3600
    )

    return {'message': 'success'}


@auth_router.post('/logout', status_code=status.HTTP_204_NO_CONTENT)
async def logout(req: Request, res: Response, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    session_id = req.cookies.get('session_id')
    if session_id:
        try:
            await delete_session(db, session_id)
        except Exception:
            pass

    res.delete_cookie('session_id')
