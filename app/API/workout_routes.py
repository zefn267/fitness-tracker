from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.CRUD.workout_operations import create_workout_op, get_all_workouts_op, get_workout_op, delete_workout_op, \
    update_workout_op
from app.db.database import get_db
from app.schemas.workout_create import WorkoutCreate
from app.schemas.workout_info import WorkoutInfo
from app.schemas.workout_update import WorkoutUpdate
from app.services.auth_service import get_current_user


workout_router = APIRouter(prefix='/api', tags=['workout'])


@workout_router.post("/workouts", response_model=WorkoutInfo, status_code=status.HTTP_201_CREATED)
async def create_workout(workout: WorkoutCreate, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    new_workout = await create_workout_op(db, workout, current_user.id)

    return new_workout


@workout_router.get('/workouts/{workout_id}', response_model=WorkoutInfo)
async def get_workout(workout_id: int, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    workout = await get_workout_op(db, workout_id, current_user.id)
    if not workout:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Workout not found')

    return workout


@workout_router.get('/workouts', response_model=list[WorkoutInfo])
async def get_all_workouts(db: AsyncSession = Depends(get_db), skip: int = 0, limit: int = 100, current_user = Depends(get_current_user)):
    workouts = await get_all_workouts_op(db, current_user.id, skip, limit)

    return workouts


@workout_router.patch('/workouts/{workout_id}', response_model=WorkoutInfo)
async def update_workout(workout_id: int, workout: WorkoutUpdate, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    result = await update_workout_op(db, workout_id, current_user.id, workout)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Workout not found')

    return result


@workout_router.delete('/workouts/{workout_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_workout(workout_id: int, db: AsyncSession = Depends(get_db), current_user: Depends = Depends(get_current_user)):
    deleted = await delete_workout_op(db, workout_id, current_user.id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Workout not found')
