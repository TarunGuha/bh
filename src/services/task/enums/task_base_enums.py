from enum import Enum


class TaskBaseEnum(Enum):

    @classmethod
    def values(cls):
        return [item.value for item in cls]

    @classmethod
    def keys(cls):
        return [item.name for item in cls]
