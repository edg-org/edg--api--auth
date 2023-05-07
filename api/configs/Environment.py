import os
from functools import lru_cache

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class EnvironmentSettings(BaseSettings):
    API_VERSION: str = os.getenv("API_VERSION")
    API_PREFIX: str = os.getenv("API_PREFIX")
    APP_NAME: str = os.getenv("APP_NAME")
    DATABASE_DIALECT: str = os.getenv("DATABASE_DIALECT")
    DATABASE_HOSTNAME: str = os.getenv("DATABASE_HOSTNAME")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME")
    DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD")
    DATABASE_PORT: int = int(os.getenv("DATABASE_PORT"))
    DATABASE_USERNAME: str = os.getenv("DATABASE_USERNAME")
    DEBUG_MODE: bool = bool(os.getenv("DEBUG_MODE"))
    JWT_SECRET_BEARER: str = os.getenv("JWT_SECRET_BEARER")
    JWT_SECRET_REFRESH: str = os.getenv("JWT_SECRET_REFRESH")
    JWT_SECRET_FORGOT_PASSWORD: str = os.getenv("JWT_SECRET_FORGOT_PASSWORD")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM")
    JWT_EXPIRATION_DAYS_BEARER: int = int(os.getenv("JWT_EXPIRATION_DAYS_BEARER"))
    JWT_EXPIRATION_DAYS_REFRESH: int = int(os.getenv("JWT_EXPIRATION_DAYS_REFRESH"))
    JWT_EXPIRATION_MINUTES_FORGOT_PASSWORD: int = int(os.getenv("JWT_EXPIRATION_MINUTES_FORGOT_PASSWORD"))

    class Config:
        env_file = ".env.dev"
        env_file_encoding = "utf-8"


@lru_cache
def get_environment_variables():
    return EnvironmentSettings()


env = get_environment_variables()