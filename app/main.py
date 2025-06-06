from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from pathlib import Path
from app.routers import worker as ui_worker_router
from app.middleware import RedirectUnauthorizedMiddleware

# Импорт маршрутов
from app.api import auth
from app.api.site import router as site_router
from app.api.subgroup import router as subgroup_router
from app.api.salary import router as salary_router
from app.api.purchase import router as purchase_router
from app.api.tool_transfer import router as tool_transfer_router
from app.api.material import router as material_router
from app.api.expense import router as expense_router
from app.api.tool import router as tool_router
from app.api.worker import router as worker_router
from app.api.auth import router as auth_router
from app.routers.pages import router as pages_router
from app.routers.form_routes import router as form_router

app = FastAPI(title="СтройКонтроль", redirect_slashes=True)
app.add_middleware(RedirectUnauthorizedMiddleware)

# Подключение API маршрутов
app.include_router(auth.router, prefix="/api/auth")  # 🔧 исправлено
app.include_router(site_router, prefix="/api")
app.include_router(subgroup_router, prefix="/api")
app.include_router(salary_router, prefix="/api")
app.include_router(purchase_router, prefix="/api")
app.include_router(tool_transfer_router, prefix="/api")
app.include_router(material_router, prefix="/api")
app.include_router(expense_router, prefix="/api")
app.include_router(tool_router, prefix="/api")
app.include_router(worker_router, prefix="/api")

# Интерфейсные и формовые маршруты
app.include_router(form_router)
app.include_router(pages_router)
app.include_router(ui_worker_router.router)

# Подключение статики и шаблонов
BASE_DIR = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Разрешение CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

