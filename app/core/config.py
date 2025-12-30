from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseSettings):
    app_name: str
    admin_email: str = "admin@example.com"
    items_per_page: int = 50
    DATABASE_URL: str
    jwt_secret_key : str
    jwt_algorithm : str
    jwt_expire_minutes : int
    REFRESH_EXPIRE_MINUTES : int


    class Config:
        env_file = ".env"
        case_sensitive=False

settings = Settings()
