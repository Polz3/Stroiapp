from app.main import app
from app.database.db import create_db

if __name__ == "__main__":
    # Создание базы данных при старте (если ещё не создана)
    create_db()
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )
