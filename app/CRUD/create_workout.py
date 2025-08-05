from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.workout_create import WorkoutCreate
from app.models.workout import Workout


async def create_workout(db: AsyncSession, workout: WorkoutCreate):
    new_workout = Workout(
        date=workout.date,
        description=workout.description
    )

    db.add(new_workout)

    await db.commit()
    await db.refresh(new_workout)

    return new_workout