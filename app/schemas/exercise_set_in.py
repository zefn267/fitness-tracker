from pydantic import BaseModel, field_validator


class ExerciseSetIn(BaseModel):
    position: int
    reps: int
    rpe: int
    rest_seconds: int
    weight: float

    @field_validator('position')
    def validate_position(cls, v: int):
        if v < 1:
            raise ValueError('position must be >= 1')
        return v

    @field_validator('reps')
    def validate_reps(cls, v: int):
        if v < 0:
            raise ValueError('reps must be >= 0')
        return v

    @field_validator('rpe')
    def validate_rpe(cls, v: int):
        if not (1 <= v <= 10):
            raise ValueError('rpe must be between 1 and 10')
        return v

    @field_validator('rest_seconds')
    def validate_rest_seconds(cls, v: int):
        if v < 0:
            raise ValueError('rest_seconds must be >= 0')
        return v

    @field_validator('weight')
    def validate_weight(cls, v: float):
        if v < 0:
            raise ValueError('weight must be >= 0')
        return v
