from pydantic import BaseModel, Base64Str


class AuthLoginRequest(BaseModel):
    login: str
    password: str


class AuthLoginResponse(BaseModel):
    token: Base64Str
    refresh: Base64Str


class AuthRegisterRequest(BaseModel):
    username: str
    password: str


class AuthRegisterResponse(BaseModel):
    id: int
    username: str
    password: str


class XToken(BaseModel):
    id: int
    value: str
