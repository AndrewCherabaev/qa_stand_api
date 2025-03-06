from __future__ import annotations

from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import types as sa_types


class AuthToken(SQLModel, table=True):
    __tablename__ = 'auth_tokens'
    id: int | None = Field(default=None, primary_key=True)
    token: str

    user: User = Relationship(back_populates='token')


class User(SQLModel, table=True):
    __tablename__ = 'users'
    id: int | None = Field(default=None, primary_key=True)
    username: str
    password: str
    is_comments_available: bool = Field(False)
    max_post_count: int = Field(3)

    token_id: int | None = Field(default=None, foreign_key='auth_tokens.id')
    token: AuthToken = Relationship(back_populates='user')


class Post(SQLModel, table=True):
    __tablename__ = 'posts'
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(sa_type=sa_types.VARCHAR, max_length=255)
    content: str = Field(sa_type=sa_types.TEXT)
    author: str
    tags: str
    likes: int | None = Field(0)
    dislikes: int | None = Field(0)


class Comment(SQLModel, table=True):
    __tablename__ = 'comments'
    id: int | None = Field(default=None, primary_key=True)
    author_id: int
    post_id: int
    content: str = Field(sa_type=sa_types.VARCHAR, max_length=255)
