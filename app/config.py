import os
from typing import Optional, Dict, Any

from dotenv import load_dotenv
from pathlib import Path
from pydantic import Field, field_validator, MongoDsn, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from functools import lru_cache

load_dotenv()


class Settings(BaseSettings):
    """
    Класс настроек.
    """
    model_config = SettingsConfigDict(env_file="../.env", env_file_encoding='utf-8', extra_fields_behavior='extra')
    MONGO_DB: str = Field(default="mongo_db")
    MONGO_URL: str = Field(default="mongodb: // localhost")
    MONGO_USER: str = Field(default="admin")
    MONGO_PASSWORD: str = Field(default="admin")
    MONGO_HOST: str = "mongodb"
    MONGO_PORT: str = '27017'
    MAX_CONNECTIONS_COUNT: int = Field(default=10)
    MIN_CONNECTIONS_COUNT: int = Field(default=3)
    MONGO_URI: str | None = None

    @model_validator(mode="after")
    def validator(self) -> "Settings":
        self.MONGO_URI = (
            f"mongodb://"
            f"{self.MONGO_USER}:"
            f"{self.MONGO_PASSWORD}@"
            f"{self.MONGO_HOST}:{self.MONGO_PORT}"
        )
        return self

    @classmethod
    def get_path(cls, path: Path) -> Path:
        file_path = Path(__file__).parent / path
        file_path.mkdir(exist_ok=True, parents=True)
        abs_path = file_path.absolute()
        return abs_path


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings: Settings = get_settings()
