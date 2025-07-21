from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, RedirectResponse
from urllib.parse import quote

class RedirectUnauthorizedMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        path = request.url.path

        # Разрешаем доступ к страницам логина и регистрации
        if path.startswith("/login") or path.startswith("/register"):
            return await call_next(request)

        # Разрешаем все API-запросы и статические файлы
        if path.startswith("/api/") or path.startswith("/static/"):
            return await call_next(request)

        # Выполняем основной запрос
        response = await call_next(request)

        # Редиректим только HTML-запросы с ошибкой 401
        is_html_page = request.headers.get("accept", "").startswith("text/html")
        if response.status_code == 401 and is_html_page:
            from urllib.parse import quote
            next_path = quote(path)
            return RedirectResponse(url=f"/login?next={next_path}")

        return response

