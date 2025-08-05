from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.CRUD.create_exercise import create_exercise
from app.db.database import get_db
from app.schemas.exercise_create import ExerciseCreate

router = APIRouter(prefix="/workouts/{workout_id}/exercises", tags=["exercise"])

@router.post("/", response_model=ExerciseCreate)
async def c_exercise(workout_id: int, exercise: ExerciseCreate, db: AsyncSession = Depends(get_db)):
    from app.CRUD.get_workout import get_workout
    if not await get_workout(db, workout_id):
        raise HTTPException(404, "Workout not found")

    new_exercise = await create_exercise(db, exercise, workout_id)

    return new_exercise
