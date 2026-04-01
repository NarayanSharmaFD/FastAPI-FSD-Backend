from pydantic import BaseSettings, AnyHttpUrl
from typing import List
from pathlib import Path

class Settings(BaseSettings):
    PROJECT_NAME: str = "Task Tracker"
    ENV: str = "development"

    DATABASE_URL: str

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost:3000"]

    class Config:
        env_file = str(Path(__file__).parent.parent.parent / ".env")
        env_file_encoding = "utf-8"

settings = Settings()
