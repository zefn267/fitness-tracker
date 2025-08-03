from pydantic import BaseModel, ConfigDict


class ExerciseInfo(BaseModel):
    id: int

    model_config = ConfigDict(from_attributes=True)