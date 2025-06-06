from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, RedirectResponse
from urllib.parse import quote

class RedirectUnauthorizedMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        # 🚫 Не трогаем саму страницу /login (чтобы не зациклить редирект)
        if request.url.path.startswith("/login"):
            return await call_next(request)

        # Выполняем основной запрос
        response = await call_next(request)

        # Если ответ — HTML-страница с 401, перенаправляем на /login
        is_html_page = request.headers.get("accept", "").startswith("text/html")
        if response.status_code == 401 and is_html_page:
            next_path = quote(request.url.path)
            return RedirectResponse(url=f"/login?next={next_path}")

        return response
