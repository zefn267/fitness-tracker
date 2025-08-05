from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.workout import Workout


async def get_all_workouts(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(Workout)
        .order_by(Workout.date.desc())
        .offset(skip)
        .limit(limit)
    )

    return result.scalars().all()