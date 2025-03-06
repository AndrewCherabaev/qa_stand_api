from typing import List, Annotated

from fastapi import APIRouter, Cookie

from api.comments.models import CommentCreateRequest, CommentResponse
from api.database.database import Repository
from api.database.entities import Comment, User, AuthToken
from api.swagger import Tags

comments_router = APIRouter(
    prefix='/comments',
    tags=[Tags.COMMENTS]
)


@comments_router.get(
    "/",
    description="Список комментов",
    response_model=List[CommentResponse]
)
async def list_comments(
        post_id: int,
        comments_repo: Annotated[Repository, Repository.of(Comment)],
):
    return comments_repo.find_all(
        Comment.post_id == post_id,
        order_by=Comment.id.desc()
    )


@comments_router.post(
    "/",
    description="Добавить коммент",
    response_model=CommentResponse
)
async def create_comments(
        auth_token: Annotated[str | None, Cookie()],
        request: CommentCreateRequest,
        comments_repo: Annotated[Repository, Repository.of(Comment)],
        users_repo: Annotated[Repository, Repository.of(User)],
        tokens_repo: Annotated[Repository, Repository.of(AuthToken)],
):
    token = tokens_repo.find(AuthToken.token == auth_token)
    user = users_repo.find(User.token_id == token.id)

    comment = Comment(
        author_id=user.id,
        post_id=request.post_id,
        content=request.content
    )

    comments_repo.create(comment)

    return comment
