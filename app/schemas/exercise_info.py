from pydantic import BaseModel


class ExerciseInfo(BaseModel):
    id: int

    class Config:
        orm_mode = True