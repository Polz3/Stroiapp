# app/auth_backend.py
from typing import Optional
from jose import JWTError, jwt
from starlette.authentication import (
    AuthenticationBackend, AuthCredentials, BaseUser, AuthenticationError
)
from starlette.requests import HTTPConnection
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
        # Достаём JWT из cookie
        token = conn.cookies.get("access_token")
        if not token:
            return  # неавторизован — пусть дойдёт до middleware

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            user_id = payload.get("sub")
            username = payload.get("username")
            if user_id is None or username is None:
                raise AuthenticationError("Invalid token payload")

            # ВАЖНО: id из JWT приходит как строка — приводим к int,
            # иначе запрос к БД не найдёт пользователя и будет вечный редирект.
            try:
                user_id_int = int(user_id)
            except (TypeError, ValueError):
                raise AuthenticationError("Invalid user id in token")

            db = SessionLocal()
            try:
                user: Optional[User] = crud_user.get_user_by_id(db, user_id_int)
                if not user:
                    raise AuthenticationError("User not found")

                return AuthCredentials(["authenticated"]), SimpleUser(
                    username=user.username,
                    user_id=user.id
                )
            finally:
                db.close()

        except JWTError:
            raise AuthenticationError("Invalid JWT token")
