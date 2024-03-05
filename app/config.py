from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings


class CommonSettings(BaseSettings):
    DEBUG_MODE: bool = Field(default=True)
    SECRET_KEY: str = Field(default="secret")
    JWT_ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60)
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=14)



class RabbitMQSettings(BaseSettings):
    RABBITMQ_HOST: str = Field(default="localhost")
    RABBITMQ_PORT: str = Field(default="5672")
    RABBITMQ_USER: str = Field(default="user")
    RABBITMQ_PASSWORD: str = Field(default="pass")



class DBSettings(BaseSettings):
    DB_HOST: str = Field(default="localhost")
    DB_PORT: int = Field(default=3306)
    DB_DATABASE: str = Field(default="whelptask")
    DB_USER: str = Field(default="whelp_user")
    DB_PASSWORD: str = Field(default="userpass")


class ThirdPartySettings(BaseSettings):
    IPDATA_API_KEY: str = Field(default="")



class Settings(
    CommonSettings,
    DBSettings,
    RabbitMQSettings,
    ThirdPartySettings
):
    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
