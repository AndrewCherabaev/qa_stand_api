from typing import NoReturn, Annotated
from uuid import uuid4

from fastapi import APIRouter, HTTPException, Response, Cookie

from api.auth.models import AuthLoginRequest, AuthLoginResponse, AuthRegisterRequest, AuthRegisterResponse
from api.database.database import Repository
from api.database.entities import AuthToken, User
from api.swagger import Tags, OkResponse

auth_router = APIRouter(
    prefix='/auth',
    tags=[Tags.AUTH]
)


@auth_router.post("/register", description="Регистрация", response_model=AuthRegisterResponse)
async def register(
        request: AuthRegisterRequest,
        user_repo: Annotated[Repository, Repository.of(User)],
        token_repo: Annotated[Repository, Repository.of(AuthToken)],
        response: Response
):
    token = AuthToken(token=str(uuid4()))
    token_repo.create(token)

    user = User(
        username=request.username,
        password=request.password,
        token_id=token.id,
    )

    user_repo.create(user)

    response.set_cookie(key='auth_token', value=token.token)

    return user


@auth_router.post(
    "/login",
    description="Логин",
    response_model=AuthLoginResponse
)
async def login(_request: AuthLoginRequest) -> NoReturn:
    raise HTTPException(
        status_code=304,
        detail="""
        Error 500 from %env.cluster.keycloak%:
        'Invalid user credentials'
        """
    )


@auth_router.get("/logout", description="Логаут", response_model=OkResponse)
async def logout(
        auth_token: Annotated[str | None, Cookie()],
        user_repo: Annotated[Repository, Repository.of(User)],
        token_repo: Annotated[Repository, Repository.of(AuthToken)],
):
    token = token_repo.find(AuthToken.token == auth_token)
    user = user_repo.find(User.token_id == token.id)

    user.token_id = None
    user_repo.save(user)

    token_repo.delete(AuthToken.token == auth_token)

    return {}
