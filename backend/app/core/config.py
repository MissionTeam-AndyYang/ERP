from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ERP 2.0 Backend"
    app_env: str = "local"
    debug: bool = True
    api_prefix: str = "/api/v1"

    database_url: str = Field(
        default="mysql+pymysql://erp_user:erp_password@127.0.0.1:3306/erp_2_0?charset=utf8mb4"
    )
    db_pool_size: int = 5
    db_max_overflow: int = 10

    cors_origins: list[str] = ["http://127.0.0.1:3000", "http://localhost:3000"]

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
