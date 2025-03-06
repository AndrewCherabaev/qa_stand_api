from typing import Annotated

from fastapi import APIRouter, Cookie
from fastapi.responses import JSONResponse

from api.auth.models import XToken
from api.database.database import Repository
from api.database.entities import User, AuthToken
from api.swagger import Tags, OkResponse
from api.users.models import (
    UserEditRequest,
    UserEditResponse,
    UserEditSettingsRequest,
    UserEditSettingsResponse,
    UserResponse,
)

users_router = APIRouter(
    prefix='/users',
    tags=[Tags.USERS]
)


@users_router.get(
    "/me",
    description="Текущий пользователь",
    response_model=UserResponse
)
async def me(
        auth_token: Annotated[str | None, Cookie()],
        user_repo: Annotated[Repository, Repository.of(User)],
        token_repo: Annotated[Repository, Repository.of(AuthToken)],
):
    token = token_repo.find(AuthToken.token == auth_token)
    user = user_repo.find(User.token_id == token.id)

    return UserResponse(
        id=user.id,
        name=user.username,
        password=user.password,
        email='',
        is_comments_available=user.is_comments_available,
        max_post_count=user.max_post_count,
        auth_token=XToken(
            id=token.id,
            value=token.token
        )
    )


@users_router.post(
    "/edit/profile",
    description="Редактировать пользователя",
    response_model=UserEditResponse
)
async def me_edit_profile(
        _auth_token: Annotated[str | None, Cookie(alias='auth_token')],
        _request: UserEditRequest
):
    return JSONResponse(OkResponse().model_dump())


@users_router.post(
    "/edit/settings",
    description="Редактировать настройки пользователя",
    response_model=UserEditSettingsResponse
)
async def me_edit_settings(
        request: UserEditSettingsRequest,
        auth_token: Annotated[str | None, Cookie()],
        user_repo: Annotated[Repository, Repository.of(User)],
        token_repo: Annotated[Repository, Repository.of(AuthToken)],

):
    token = token_repo.find(AuthToken.token == auth_token)
    user = user_repo.find(User.token_id == token.id)

    user.is_comments_available = request.is_comments_available
    user.max_post_count = request.max_post_count

    user_repo.save(user)

    return request
