from typing import Annotated, List

from fastapi import APIRouter, HTTPException, Query, Cookie
from fastapi.responses import JSONResponse

from api.database.database import Repository
from api.database.entities import Post, User, AuthToken
from api.posts.models import PostCreateRequest, PostResponse, PostReactionCreateResponse
from api.swagger import Tags, OkResponse

posts_router = APIRouter(
    prefix='/posts',
    tags=[Tags.POSTS]
)


@posts_router.get(
    "/",
    description="Список постов",
    response_model=List[PostResponse]
)
async def list_post(
        posts_repo: Annotated[Repository, Repository.of(Post)],
        search: str = '',
        author: str = '',
):
    q = []
    if search:
        q.append(Post.title.like(f"%{search}%"))
    if author:
        q.append(Post.author == author)

    return posts_repo.find_all(*q)


@posts_router.post(
    "/",
    description="Создать пост",
    response_model=PostResponse
)
async def create_post(
        auth_token: Annotated[str | None, Cookie()],
        request: PostCreateRequest,
        posts_repo: Annotated[Repository, Repository.of(Post)],
        tokens_repo: Annotated[Repository, Repository.of(AuthToken)],
        users_repo: Annotated[Repository, Repository.of(User)],
):
    if not auth_token:
        raise HTTPException(401)

    token = tokens_repo.find(AuthToken.token == auth_token)
    user = users_repo.find(User.token_id == token.id)
    if len(posts_repo.find_all(Post.author == user.username)) >= user.max_post_count:
        user.token_id = None
        users_repo.save(user)

        tokens_repo.delete(AuthToken.token == auth_token)

        raise HTTPException(500, "Превышен лимит публикации для бесплатного тарифа")

    post = Post(
        title=request.title,
        content=request.content,
        author=request.author,
        tags=' '.join(request.tags),
    )

    posts_repo.create(post)

    return post


@posts_router.get("/{post_id}", description="Получить пост", response_model=PostResponse)
async def get_post(
        post_id: int,
        posts_repo: Annotated[Repository, Repository.of(Post)],
):
    return posts_repo.find(Post.id == post_id)


@posts_router.post(
    "/{post_id}/likes",
    description="Лайкнуть пост",
    response_model=OkResponse | PostReactionCreateResponse
)
async def like_post(
        post_id: int,
        auth_token: Annotated[str | None, Cookie()],
        posts_repo: Annotated[Repository, Repository.of(Post)],
        items: Annotated[bool, Query(description='Вернуть список вместо инкремента')] = False,
):
    """
    Если передан параметр items - возвращать список, иначе - ставить лайк
    """
    if not auth_token:
        raise HTTPException(401)

    post = posts_repo.find(Post.id == post_id)

    res = PostReactionCreateResponse(
        post_id=post_id,
        count=post.likes if items else post.likes+1,
    )

    if not items:
        post.likes = post.likes + 1
        posts_repo.save(post)

    return res


@posts_router.post(
    "/{post_id}/dislikes",
    description="Дизайкнуть пост",
    response_model=OkResponse | PostReactionCreateResponse
)
async def dislike_post(
        post_id: int,
        auth_token: Annotated[str | None, Cookie()],
        posts_repo: Annotated[Repository, Repository.of(Post)],
        items: Annotated[bool, Query(description='Вернуть список вместо инкремента')] = False
):
    """
    Если передан параметр items - возвращать список, иначе - ставить дизлайк
    Должен не работать на проставление дизлайка
    """
    if not auth_token:
        raise HTTPException(401)

    if not items:
        raise HTTPException(
            status_code=500,
            detail="Something went wrong"
        )

    post = posts_repo.find(Post.id == post_id)

    return PostReactionCreateResponse(
        post_id=post_id,
        count=post.likes,
    )
