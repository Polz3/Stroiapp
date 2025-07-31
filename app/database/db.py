from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

# URL для SQLite базы данных
SQLALCHEMY_DATABASE_URL = "sqlite:///instance/database.db"

# Создание движка
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # Только для SQLite
)

# Создание фабрики сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс моделей
Base = declarative_base()

# Зависимость FastAPI — получение сессии БД
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_db() -> None:
    """
    Создает все таблицы, описанные в моделях SQLAlchemy.
    При этом удаляет старые таблицы и создаёт схему заново.
    """
    # Импортируем модели, чтобы зарегистрировать их в metadata
    import app.models.models     # определяет Subgroup, Site, Material, Worker, Tool, Expense, ToolTransfer
    import app.models.salary     # определяет модель Salary

    # Удаляем старые таблицы (если они существуют) и создаём новые
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
