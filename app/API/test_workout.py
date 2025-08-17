from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.CRUD.workout_operations import create_workout, get_all_workouts, get_workout
from app.db.database import get_db
from app.schemas.workout_create import WorkoutCreate
from app.schemas.workout_info import WorkoutInfo
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/workout", tags=["workout"])

@router.post("/", response_model=WorkoutCreate)
async def register_user(workout: WorkoutCreate, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    new_workout = await create_workout(db, workout, current_user.id)

    return new_workout


@router.get("/workout/{workout_id}", response_model=WorkoutInfo)
async def get_user_info(workout_id: int, db: AsyncSession = Depends(get_db)):
    workout = await get_workout(db, workout_id)
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")

    return workout


@router.get("/all_workouts", response_model=list[WorkoutCreate])
async def get_all(db: AsyncSession = Depends(get_db), skip: int = 0, limit: int = 100):
    workouts = await get_all_workouts(db, skip, limit)

    return workouts