from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.schemas.workout_create import WorkoutCreate
from app.models.workout import Workout


async def create_workout(db: AsyncSession, workout: WorkoutCreate, user_id: int):
    new_workout = Workout(
        user_id=user_id,
        name=workout.name,
        date=workout.date,
        workout_type=workout.workout_type,
        description=workout.description,
    )

    db.add(new_workout)

    await db.commit()
    await db.refresh(new_workout)

    return new_workout


async def get_workout(db: AsyncSession, workout_id: int):
    result = await db.execute(
        select(Workout)
        .options(selectinload(Workout.exercises))
        .where(Workout.id == workout_id)
    )

    return result.scalar_one_or_none()


async def get_all_workouts(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(Workout)
        .order_by(Workout.date.desc())
        .offset(skip)
        .limit(limit)
    )

    return result.scalars().all()
