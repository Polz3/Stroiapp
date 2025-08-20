from pathlib import Path
from typing import Generator

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session, declarative_base

# === Абсолютный путь к БД + автосоздание каталога instance ===
# BASE_DIR → папка app/
BASE_DIR = Path(__file__).resolve().parent.parent
DB_DIR = (BASE_DIR / ".." / "instance").resolve()
DB_DIR.mkdir(parents=True, exist_ok=True)

SQLALCHEMY_DATABASE_URL = f"sqlite:///{(DB_DIR / 'database.db').as_posix()}"

# === Движок SQLAlchemy ===
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},  # для SQLite в одном процессе
    pool_pre_ping=True,                         # живой коннект перед запросом
)

# Рекомендуемые PRAGMA для снижения блокировок и подвисаний записи
with engine.connect() as conn:
    try:
        conn.execute(text("PRAGMA journal_mode=WAL;"))
        conn.execute(text("PRAGMA busy_timeout=5000;"))
    except Exception:
        # На некоторых платформах PRAGMA могут быть недоступны — просто пропускаем
        pass

# === Сессии и базовый класс ===
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# === Зависимость FastAPI — сессия БД ===
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_db() -> None:
    """
    Пере-создаёт схему БД на основе моделей SQLAlchemy.
    ВНИМАНИЕ: удаляет таблицы (drop_all) — используйте только для локальных тестов!
    Для сервера применяйте миграции Alembic: `alembic upgrade head`.
    """
    # Импортируем модели, чтобы зарегистрировать их в metadata
    import app.models.models     # Subgroup, Site, Material, Worker, Tool, Expense, ToolTransfer

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
