from pydantic import BaseModel, field_validator


class ExerciseSetIn(BaseModel):
    position: int
    reps: int
    rpe: int
    rest_seconds: int
    weight: float

    @staticmethod
    @field_validator('position')
    def validate_position(v):
        if v < 1:
            raise ValueError('position must be >= 1')
        return v

    @staticmethod
    @field_validator('reps')
    def validate_reps(v):
        if v < 0:
            raise ValueError('reps must be >= 0')
        return v

    @staticmethod
    @field_validator('rpe')
    def validate_rpe(v):
        if not (1 <= v <= 10):
            raise ValueError('rpe must be between 1 and 10')
        return v

    @staticmethod
    @field_validator('rest_seconds')
    def validate_rest_seconds(v):
        if v < 0:
            raise ValueError('rest_seconds must be >= 0')
        return v