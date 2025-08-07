# app/core/config.py

# Поддержка и Pydantic v1, и v2 (на будущее):
try:
    # Если позже перейдёте на pydantic v2 и добавите пакет pydantic-settings,
    # этот импорт будет работать.
    from pydantic_settings import BaseSettings  # type: ignore
except ImportError:
    # Текущий рабочий вариант для pydantic==1.10.13
    from pydantic import BaseSettings


class Settings(BaseSettings):
    # Обязательные/важные настройки
    SECRET_KEY: str = "change-me"   # переопределите через переменные окружения на Render
    ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
