from fastapi import FastAPI
from starlette.middleware.authentication import AuthenticationMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from pathlib import Path

# 🔐 Auth / middleware
from app.auth_backend import JWTAuthBackend
from app.middleware import RedirectUnauthorizedMiddleware

# 🔌 API routers
from app.api.auth import router as auth_router
from app.api.site import router as site_router
from app.api.subgroup import router as subgroup_router
from app.api.salary import router as salary_router
from app.api.expense import router as expense_router
from app.api.tool_transfer import router as tool_transfer_router
from app.api.material import router as material_router
from app.api.tool import router as tool_router
from app.api.worker import router as worker_router

# 🖼 UI routers
from app.routers.pages import router as pages_router
from app.routers.form_routes import router as form_router
from app.routers.worker import router as ui_worker_router  # UI-страницы для сотрудников

app = FastAPI(
    title="СтройКонтроль",
    redirect_slashes=False
)

# 🌍 CORS (по необходимости можно сузить домены)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔐 JWT + редирект неавторизованных
app.add_middleware(RedirectUnauthorizedMiddleware)
app.add_middleware(AuthenticationMiddleware, backend=JWTAuthBackend())

# 🗂 Статика и шаблоны
BASE_DIR = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# 🔌 API
app.include_router(auth_router, tags=["auth"])
app.include_router(site_router, tags=["sites"])
app.include_router(subgroup_router, tags=["subgroups"])
app.include_router(worker_router, tags=["workers"])
app.include_router(salary_router, tags=["salaries"])
app.include_router(expense_router, tags=["expenses"])  # единый GET /api/expenses/
app.include_router(tool_router, tags=["tools"])
app.include_router(tool_transfer_router, tags=["tool_transfers"])
app.include_router(material_router, tags=["materials"])

# 🖼 UI
app.include_router(pages_router)
app.include_router(form_router)
app.include_router(ui_worker_router)
