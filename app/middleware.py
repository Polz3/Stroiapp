from starlette.responses import RedirectResponse
from starlette.requests import Request
from starlette.types import ASGIApp, Receive, Scope, Send
from urllib.parse import quote

class RedirectUnauthorizedMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive=receive)

        path = request.url.path
        accept = request.headers.get("accept", "")
        is_html = accept.startswith("text/html")

        allowed = path.startswith(("/login", "/register", "/static", "/api"))

        # 🧠 Проверяем, авторизован ли пользователь
        try:
            user = request.user
            is_authenticated = getattr(user, "is_authenticated", False)
        except AssertionError:
            is_authenticated = False

        if not allowed and is_html and not is_authenticated:
            next_path = quote(path)
            response = RedirectResponse(url=f"/login?next={next_path}")
            await response(scope, receive, send)
        else:
            await self.app(scope, receive, send)
