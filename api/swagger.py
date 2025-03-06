from enum import StrEnum, auto

from pydantic import BaseModel


class CapitalStrEnum(StrEnum):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return name.capitalize()


class Tags(CapitalStrEnum):
    AUTH = auto()
    POSTS = auto()
    COMMENTS = auto()
    USERS = auto()


class OkResponse(BaseModel):
    status: str = 'ok'
