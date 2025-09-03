from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.schemas.workout_create import WorkoutCreate
from app.models.workout import Workout
from app.schemas.workout_update import WorkoutUpdate


async def create_workout_op(db: AsyncSession, workout: WorkoutCreate, user_id: int):
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


async def get_workout_op(db: AsyncSession, workout_id: int, user_id: int):
    result = await db.execute(
        select(Workout)
        .options(selectinload(Workout.exercises))
        .where(Workout.id == workout_id, Workout.user_id == user_id)
    )

    return result.scalar_one_or_none()


async def get_all_workouts_op(db: AsyncSession, user_id: int, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(Workout)
        .where(Workout.user_id == user_id)
        .order_by(Workout.date.desc())
        .offset(skip)
        .limit(limit)
    )

    return result.scalars().all()


async def update_workout_op(db: AsyncSession, workout_id: int, user_id: int, data: WorkoutUpdate):
    data = data.model_dump(exclude_unset=True)
    if not data:
        return await db.scalar(
            select(Workout)
            .where(Workout.user_id == user_id, Workout.id == workout_id)
        )

    result = await db.execute(
        update(Workout)
        .where(Workout.id == workout_id, Workout.user_id == user_id)
        .values(**data)
        .returning(Workout)
    )

    await db.commit()

    return result.scalar_one_or_none()


async def delete_workout_op(db: AsyncSession, workout_id: int, user_id: int):
    result = await db.execute(
        delete(Workout)
        .where(Workout.id == workout_id, Workout.user_id == user_id)
        .returning(Workout.id)
    )

    await db.commit()

    return result.scalar_one_or_none() is not None
