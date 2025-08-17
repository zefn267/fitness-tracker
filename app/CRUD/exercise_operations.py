from sqlalchemy import select, func, update, delete, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.exercise_set import ExerciseSet
from app.models.exercise import Exercise
from app.schemas.exercise_create import ExerciseCreate
from app.schemas.exercise_info import ExerciseInfo
from app.schemas.exercise_set_in import ExerciseSetIn
from app.schemas.exercise_stats_out import ExerciseStatsOut


async def _count_sets(db: AsyncSession, exercise_id: int) -> int:
    return await db.scalar(select(func.count(ExerciseSet.id)).where(ExerciseSet.exercise_id == exercise_id))


async def _load_exercise_info(db: AsyncSession, exercise_id: int) -> ExerciseInfo:
    exercise = (await db.execute(
        select(Exercise)
        .options(selectinload(Exercise.sets))
        .where(Exercise.id == exercise_id)
        )
    ).scalar_one_or_none()
    if not exercise:
        raise ValueError('Exercise not found')

    sets = [
        ExerciseSetIn(
            position=s.position,
            reps=s.reps,
            rpe=s.rpe,
            rest_seconds=s.rest_seconds,
            weight=s.weight
        )
        for s in exercise.sets
    ]

    return ExerciseInfo(
        id=exercise.id,
        name=exercise.name,
        workout_id=exercise.workout_id,
        description=exercise.description,
        sets=sorted(sets, key=lambda s: s.position),
    )


async def create_exercise(db: AsyncSession, data: ExerciseCreate) -> ExerciseInfo:
    exercise = Exercise(
        name=data.name,
        description=data.description,
        workout_id=data.workout_id,
    )
    exercise.sets = [
        ExerciseSet(
            position=s.position,
            reps=s.reps,
            rpe=s.rpe,
            rest_seconds=s.rest_seconds,
            weight=s.weight
        )
        for s in data.sets
    ]

    db.add(exercise)
    await db.commit()

    return await _load_exercise_info(db, exercise.id)


async def get_exercise_info(db: AsyncSession, exercise_id: int) -> ExerciseInfo:
    return await _load_exercise_info(db, exercise_id)


async def update_set_by_position(
        db: AsyncSession,
        exercise_id: int,
        position: int,
        *,
        reps: int | None = None,
        rpe: int | None = None,
        rest_seconds: int | None = None,
        weight: float | None = None
) -> ExerciseInfo:
    values = {}
    if reps is not None:
        values['reps'] = reps
    if rpe:
        values['rpe'] = rpe
    if rest_seconds is not None:
        values['rest_seconds'] = rest_seconds
    if weight is not None:
        values['weight'] = weight

    if values:
        await db.execute(
            update(ExerciseSet)
            .where(ExerciseSet.exercise_id == exercise_id, ExerciseSet.position == position)
            .values(**values)
        )

    await db.commit()

    return await _load_exercise_info(db, exercise_id)


async def delete_last_set(
        db: AsyncSession,
        exercise_id: int,
        *,
        allow_delete_exercise: bool = False
)-> ExerciseInfo | None:
    async with db.begin():
        count = await _count_sets(db, exercise_id)
        if count == 0:
            raise ValueError('exercise has no sets')
        if count == 1:
            if not allow_delete_exercise:
                raise ValueError('Cannot delete the last set')
            await db.execute(delete(Exercise).where(Exercise.id == exercise_id))
            return None

        max_pos = await db.scalar(
            select(func.max(ExerciseSet.position))
            .where(ExerciseSet.exercise_id == exercise_id)
        )
        await db.execute(
            delete(ExerciseSet)
            .where(ExerciseSet.exercise_id == exercise_id, ExerciseSet.position == max_pos)
        )

    return await _load_exercise_info(db, exercise_id)

async def get_exercises_stats(db: AsyncSession, workout_id: int) -> list[ExerciseStatsOut]:
    s = (
        select(
            Exercise.id,
            Exercise.name,
            func.count(ExerciseSet.id).label('sets_count'),
            func.sum(ExerciseSet.reps).label('total_reps'),
            func.avg(ExerciseSet.rest_seconds).label('avg_rest_time'),
            func.avg(ExerciseSet.rpe).label('avg_rpe')
        )
        .join(ExerciseSet, ExerciseSet.exercise_id == Exercise.id)
        .where(Exercise.workout_id == workout_id)
        .group_by(Exercise.id)
        .order_by(Exercise.id)
    )

    result = await db.execute(s)
    rows = result.mappings().all()

    return [ExerciseStatsOut(**row) for row in rows]


async def insert_set(
        db: AsyncSession,
        exercise_id: int,
        new_set: ExerciseSetIn
) -> ExerciseInfo:
    k = new_set.position
    async with db.begin():
        await db.execute(
            update(ExerciseSet)
            .where(ExerciseSet.exercise_id == exercise_id, ExerciseSet.position >= k)
            .values(position=ExerciseSet.position + 1)
        )
        await db.execute(
            insert(ExerciseSet)
            .values(
                exercise_id=exercise_id,
                position=k,
                reps=new_set.reps,
                rpe=new_set.rpe,
                rest_seconds=new_set.rest_seconds,
                weight=new_set.weight,
            )
        )

    return await _load_exercise_info(db, exercise_id)
