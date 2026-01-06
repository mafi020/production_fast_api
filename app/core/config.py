from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    APP_NAME: str
    ADMIN_EMAIL: str = "admin@example.com"
    ITEMS_PER_PAGE: int = 50
    DATABASE_URL: str
    JWT_SECRET_KEY : str
    JWT_ALGORITHM : str
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES : int
    JWT_REFRESH_EXPIRE_MINUTES : int
    CORS_ORIGINS: str
    REDIS_HOST: str
    REDIS_PORT: int


    class Config:
        env_file = ".env"
        case_sensitive=False

settings = Settings()
