from sqlalchemy.ext.asyncio import AsyncSession
from app.models.exercise import Exercise
from app.schemas.exercise_create import ExerciseCreate


async def create_exercise(db: AsyncSession, exercise: ExerciseCreate, workout_id: int):
    new_exercise = Exercise(
        name=exercise.name,
        description=exercise.description,
        workout_id=workout_id,
        weight=exercise.weight,
        sets=exercise.sets,
        reps=exercise.reps
    )

    db.add(new_exercise)

    await db.commit()
    await db.refresh(new_exercise)

    return new_exercise
