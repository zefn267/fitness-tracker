import enum


class GenderEnum(str, enum.Enum):
    MALE = 'Мужской'
    FEMALE = 'Женский'