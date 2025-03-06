from typing import List

from pydantic import BaseModel


class PostCreateRequest(BaseModel):
    author: str
    title: str
    content: str
    tags: List[str]

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Пример заголовка",
                "content": "Пример текста для поста",
                "tags": ["it"]
            }
        }


class PostResponse(PostCreateRequest):
    id: int
    tags: str


class PostReactionCreateResponse(BaseModel):
    post_id: int
    count: int
