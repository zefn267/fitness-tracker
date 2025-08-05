from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.workout import Workout


async def get_workout(db: AsyncSession, workout_id: int):
    result = await db.execute(
        select(Workout)
        .options(selectinload(Workout.exercises))
        .where(Workout.id == workout_id)
    )

    return result.scalar_one_or_none()