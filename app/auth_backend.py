from typing import Optional
from jose import JWTError, jwt
from starlette.authentication import (
    AuthenticationBackend, AuthCredentials, BaseUser, AuthenticationError
)
from starlette.requests import HTTPConnection
from datetime import datetime
from app.database.db import SessionLocal
from app.crud import user as crud_user
from app.models.models import User
from app.core.config import settings

class SimpleUser(BaseUser):
    def __init__(self, username: str, user_id: int):
        self.username = username
        self.user_id = user_id

    @property
    def is_authenticated(self) -> bool:
        return True

class JWTAuthBackend(AuthenticationBackend):
    async def authenticate(self, conn: HTTPConnection):
        # Получаем куки из запроса
        token = conn.cookies.get("access_token")
        if not token:
            print("🚫 Нет cookies в запросе")
            return

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            user_id: str = payload.get("sub")
            username: str = payload.get("username")
            if user_id is None or username is None:
                raise AuthenticationError("Invalid token payload")

            print(f"📥 user_id из токена: {user_id}")

            db = SessionLocal()
            user: Optional[User] = crud_user.get_user_by_id(db, user_id)
            if not user:
                raise AuthenticationError("User not found")

            print(f"🔎 Найденный пользователь: {user.username}")

            return AuthCredentials(["authenticated"]), SimpleUser(username=user.username, user_id=user.id)

        except JWTError:
            print("⚠️ JWT Error")
            raise AuthenticationError("Invalid JWT token")
