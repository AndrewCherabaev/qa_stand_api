from pydantic import BaseModel, Field

from api.auth.models import XToken


class UserEditRequest(BaseModel):
    name: str
    email: str
    password: str


class UserEditResponse(UserEditRequest):
    pass


class UserEditSettingsRequest(BaseModel):
    is_comments_available: bool = Field(False, description='Пользователь может комментировать посты')
    max_post_count: int = Field(3, le=20, description='Ограничиваем через платную подписку')


class UserEditSettingsResponse(UserEditSettingsRequest):
    pass


class UserResponse(UserEditResponse, UserEditSettingsResponse):
    id: int
    auth_token: XToken
