from functools import lru_cache

from typing import Optional
from pathlib import Path

from pydantic import PostgresDsn, field_validator, ValidationInfo, IPvAnyAddress, ValidationError
from pydantic_settings import BaseSettings
from pydantic_core import MultiHostUrl

BASE_DIR: Path = Path(__file__).resolve().parent.parent


class BaseConfig(BaseSettings):
    class Config:
        env_file = BASE_DIR / ".env"
        case_sensitive = True
        env_file_encoding = "utf-8"
        extra = 'ignore'


# noinspection PyNestedDecorators
class AppSettings(BaseConfig):
    APP_NAME: str
    APP_IP: str
    APP_PORT: int

    @field_validator('APP_IP', mode='before')
    @classmethod
    def assemble_ip(cls, field_value: Optional[str], values: ValidationInfo) -> str:
        if field_value == 'localhost':
            return field_value
        return str(IPvAnyAddress(field_value))

    @field_validator('APP_PORT', mode='after')
    @classmethod
    def assemble_port(cls, field_value: Optional[int], values: ValidationInfo) -> int:
        assert field_value < pow(2, 16)  # 65536
        return field_value


# noinspection PyNestedDecorators
class DatabaseSettings(BaseConfig):
    DB_HOST: str
    DB_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    DATABASE_URI: Optional[PostgresDsn] = None

    @field_validator('DATABASE_URI', mode='before')
    @classmethod
    def assemble_db_url(cls, field_value: Optional[PostgresDsn], values: ValidationInfo) -> PostgresDsn:
        if isinstance(field_value, MultiHostUrl):
            return field_value

        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=values.data.get('POSTGRES_USER'),
            password=values.data.get('POSTGRES_PASSWORD'),
            host=values.data.get('DB_HOST'),
            port=values.data.get('DB_PORT'),
            path=f"{values.data.get('POSTGRES_DB')}",
        )


@lru_cache
def get_db_settings() -> DatabaseSettings:
    return DatabaseSettings()


@lru_cache
def get_app_settings() -> AppSettings:
    return AppSettings()


# print(get_db_settings())
# print(get_app_settings())
