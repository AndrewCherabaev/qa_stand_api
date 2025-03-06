from pydantic import BaseModel, Field


class CommentCreateRequest(BaseModel):
    content: str
    post_id: int


class CommentResponse(BaseModel):
    id: int
    author_id: int | None = Field(None, serialization_alias='author')
    post_id: int = None
    content: str = None
