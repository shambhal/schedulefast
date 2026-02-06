from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    TIMEZONE: str = "Asia/Kolkata"
    DATABASE_URL: str
    ALLOWED_HOSTS:str
    class Config:
        env_file = ".env"

settings = Settings()

