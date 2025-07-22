from starlette.authentication import (
    AuthenticationBackend, AuthCredentials, UnauthenticatedUser
)
from starlette.requests import HTTPConnection
from jose import JWTError, jwt
from app.models.user import User
from app.database.db import SessionLocal
from app.core.config import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

class SimpleUser(User):
    @property
    def is_authenticated(self):
        return True

class JWTAuthBackend(AuthenticationBackend):
    async def authenticate(self, conn: HTTPConnection):
        if "cookie" not in conn.headers:
            print("🚫 Нет cookies в запросе")
            return

        token = conn.cookies.get("access_token")
        print("🍪 Headers:", conn.headers)
        print("🍪 Cookie:", token)

        if not token:
            print("🚫 Токен не найден в cookies")
            return

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id = payload.get("sub")
            print("📥 user_id из токена:", user_id)
        except JWTError as e:
            print("❌ Ошибка при декодировании JWT:", str(e))
            return

        if user_id is None:
            print("🚫 В токене нет user_id (sub)")
            return

        db = SessionLocal()
        try:
            user = db.query(User).filter(User.id == int(user_id)).first()
            if not user:
                print("❌ Пользователь не найден в базе")
                return

            print("🔎 Найденный пользователь:", user.username)
            return AuthCredentials(["authenticated"]), SimpleUser(**user.__dict__)
        finally:
            db.close()
