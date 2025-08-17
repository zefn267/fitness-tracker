from pydantic import BaseModel


class ExerciseStatsOut(BaseModel):
    id: int
    name: str
    sets_count: int
    total_reps: int
    avg_rest_time: float
    avg_rpe: float
