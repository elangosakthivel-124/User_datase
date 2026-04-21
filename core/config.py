from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    SECRET_KEY: str = Field(..., min_length=32)
    ALGORITHM: str = "HS256"

    ACCESS_EXPIRE_MINUTES: int = Field(..., gt=0)
    REFRESH_EXPIRE_DAYS: int = Field(..., gt=0)

    DATABASE_URL: str

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
