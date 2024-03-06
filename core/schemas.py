import datetime

from pydantic import BaseModel, Field
from pydantic.networks import IPvAnyAddress


class SignupSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=32)
    password: str = Field(..., min_length=8, max_length=64)


class UserResponseSchema(BaseModel):
    id: int
    username: str
    created_at: datetime.datetime


class TokensSchema(BaseModel):
    access: str
    refresh: str


class AccessTokenSchema(BaseModel):
    access: str


class ObtainAccessTokenSchema(BaseModel):
    refresh_token: str


class TaskCreate(BaseModel):
    ip: IPvAnyAddress


class TaskCreateResponse(BaseModel):
    id: int


class StatusResponse(BaseModel):
    id: int
    status: str
    ip: str
    data: dict|None