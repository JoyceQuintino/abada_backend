from typing import List
from decouple import config
from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # SECRET_KEY: str = config("SECRET_KEY", cast=str)
    # REFRESH_SECRET_KEY: str = config("REFRESH_SECRET_KEY", cast=str)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 # 7 dias
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    PROJECT_NAME: str = "ABADÁ Backend"

    # Database
    CONNECTION_STRING: str = config("DATABASE_URL", cast=str)

    class Config:
        case_sensitive = True

settings = Settings()