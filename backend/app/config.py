import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = os.getenv("SECRET_KEY", "devsecret")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./dev.db")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

settings = Settings()
