from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = "T8Kfn7_Wh04YtLNHhHHR8Kxv4NZRZhKmXc8nQqK4Zx0"
    ALGORITHM: str = "HS256"

settings = Settings()
