from fastapi import APIRouter, Request, Depends, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pathlib import Path
from datetime import datetime, date
from collections import defaultdict
from fastapi.templating import Jinja2Templates

from app.database.db import get_db
import app.crud.site as crud_site
import app.crud.subgroups as crud_sg
import app.crud.expense as crud_exp
import app.crud.salary as crud_sal
import app.crud.worker as crud_worker
import app.crud.tool as crud_tool
import app.crud.tool_transfer as crud_tr

from app.api.auth import get_current_user
from app.models.user import User
from typing import Annotated
from app.api.auth import get_optional_user

BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
router = APIRouter()

# --- Главная страница ---
@router.get("/", response_class=HTMLResponse)
def index(
    request: Request,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    sites = crud_site.get_sites(db, user_id=current_user.id)
    workers = crud_worker.get_workers(db, user_id=current_user.id)
    tools = crud_tool.get_all(db, user_id=current_user.id)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "now": datetime.now,
        "sites": sites,
        "workers": workers,
        "tools": tools
    })


# --- Объекты ---
@router.get("/sites", response_class=HTMLResponse, name="pages.sites_page")
def sites_page(request: Request):
    return templates.TemplateResponse("sites.html", {"request": request})


@router.get("/sites/archive", response_class=HTMLResponse)
def sites_archive_page(request: Request, db: Session = Depends(get_db)):
    sites = crud_site.get_sites(db, user_id=None, include_archived=True)
    return templates.TemplateResponse("sites_archive.html", {
        "request": request,
        "sites": sites
    })


@router.get("/sites/{site_id}", response_class=HTMLResponse, name="pages.site_detail")
def site_detail(request: Request, site_id: int, edit: bool = False, db: Session = Depends(get_db)):
    site = crud_site.get_site(db, site_id)
    if not site:
        raise HTTPException(404, "Site not found")
    subgroups = crud_sg.get_subgroups(db)
    return templates.TemplateResponse("site_detail.html", {
        "request": request,
        "site": site,
        "subgroups": subgroups,
        "edit": edit
    })

# --- Формы создания/редактирования объектов ---
@router.get("/sites/create", response_class=HTMLResponse)
def create_site_page(request: Request, db: Session = Depends(get_db)):
    subgroups = crud_sg.get_subgroups(db)
    return templates.TemplateResponse("site_form.html", {
        "request": request,
        "site": None,
        "subgroups": subgroups
    })

@router.get("/sites/{site_id}", response_class=HTMLResponse, name="pages.site_detail")
def site_detail(
    request: Request,
    site_id: int,
    edit: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    site = crud_site.get_site(db, site_id)
    if not site:
        raise HTTPException(404, "Site not found")

    subgroups = crud_sg.get_subgroups(db)

    expenses = crud_exp.get_expenses(db, user_id=current_user.id)
    site_expenses = [e for e in expenses if e.site_id == site_id]

    salaries = crud_sal.get_salaries(db, user_id=current_user.id)
    site_salaries = [s for s in salaries if s.site_id == site_id]

    return templates.TemplateResponse("site_detail.html", {
        "request": request,
        "site": site,
        "subgroups": subgroups,
        "edit": edit,
        "expenses": site_expenses,
        "salaries": site_salaries
    })

# --- Закупка ---
@router.get("/expenses", response_class=HTMLResponse)
def expenses_page(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    site_id: str = "",
    type: str = "",
    search: str = ""
):
    expenses = crud_exp.get_expenses(db, user_id=current_user.id)
    salaries = crud_sal.get_salaries(db, user_id=current_user.id)

    class SalaryAsExpense:
        def __init__(self, sal):
            self.id = sal.id
            self.amount = sal.amount
            self.date = sal.date
            self.comment = sal.comment or "Зарплата"
            self.site_id = sal.site_id
            self.type = "salary"
            self.site = sal.site
            self.worker = sal.worker

    salary_expenses = [SalaryAsExpense(s) for s in salaries]
    all_ops = expenses + salary_expenses

    if type == "purchase":
        all_ops = [op for op in all_ops if getattr(op, "type", "") == "purchase"]
    elif type == "salary":
        all_ops = [op for op in all_ops if getattr(op, "type", "") == "salary"]

    if site_id.isdigit():
        site_id_int = int(site_id)
        all_ops = [op for op in all_ops if op.site_id == site_id_int]
    else:
        site_id_int = None

    if search:
        all_ops = [op for op in all_ops if search.lower() in (op.comment or "").lower()]

    grouped = defaultdict(list)
    for op in all_ops:
        grouped[op.date].append(op)

    for ops in grouped.values():
        ops.sort(key=lambda x: getattr(x, "id", 0), reverse=True)

    grouped = dict(sorted(grouped.items(), key=lambda x: x[0], reverse=True))

    sites = crud_site.get_sites(db, user_id=current_user.id)

    return templates.TemplateResponse("expenses.html", {
        "request": request,
        "grouped": grouped,
        "sites": sites,
        "site_id": site_id_int,
        "type": type,
        "search": search
    })

# --- Сотрудники ---
@router.get("/workers", response_class=HTMLResponse, name="pages.workers_page")
def workers_page(request: Request):
    return templates.TemplateResponse("workers.html", {"request": request})

@router.get("/workers/{worker_id}", response_class=HTMLResponse, name="pages.worker_detail")
def worker_detail(
    request: Request,
    worker_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    worker = crud_worker.get_worker(db, worker_id)
    if not worker:
        raise HTTPException(404, "Worker not found")

    # Все зарплаты этого пользователя
    all_salaries = crud_sal.get_salaries(db, user_id=current_user.id)
    salaries = [s for s in all_salaries if s.worker_id == worker_id]

    # JSON для графика
    salaries_json = [
        {
            "id": s.id,
            "amount": s.amount,
            "date": s.date.strftime("%Y-%m-%d")
        }
        for s in salaries
    ]

    # Объекты, где он работал
    site_ids = set(s.site_id for s in salaries if s.site_id is not None)
    all_sites = crud_site.get_sites(db, user_id=current_user.id)

    active_sites = [site for site in all_sites if site.id in site_ids and not site.is_archived]
    archived_sites = [site for site in all_sites if site.id in site_ids and site.is_archived]

    return templates.TemplateResponse("worker_detail.html", {
        "request": request,
        "worker": worker,
        "salaries": salaries,
        "salaries_json": salaries_json,  # ← передаём сюда
        "active_sites": active_sites,
        "archived_sites": archived_sites
    })

# --- Склад ---
@router.get("/warehouse", response_class=HTMLResponse)
def warehouse_page(request: Request, add: int = 0, db: Session = Depends(get_db)):
    tools = crud_tool.get_all(db, user_id=current_user.id)
    transfers = crud_tr.get_all(db)
    return templates.TemplateResponse("warehouse.html", {
        "request": request,
        "tools": tools,
        "transfers": transfers,
        "add": add
    })

# --- Инструменты ---
@router.get("/tools", response_class=HTMLResponse)
def tools_page(request: Request):
    return templates.TemplateResponse("tools.html", {"request": request})


# --- Материалы ---
@router.get("/materials", response_class=HTMLResponse)
def materials_page(request: Request):
    return templates.TemplateResponse("materials.html", {"request": request})

# --- Статистика ---
@router.get("/stats", response_class=HTMLResponse)
def stats_page(request: Request):
    return templates.TemplateResponse("stats.html", {"request": request})

# --- Зарплата ---
@router.post("/api/salaries", name="form.create_salary")
def create_salary(amount: float = Form(...), site_id: int = Form(...), worker_id: int = Form(...), comment: str = Form(""), date: datetime = Form(...), db: Session = Depends(get_db)):
    crud_sal.create_salary(db=db, amount=amount, site_id=site_id, worker_id=worker_id, comment=comment, date=date)
    return RedirectResponse("/", status_code=303)

# --- Перемещение инструмента ---
@router.post("/api/tool_transfers", name="form.create_tool_transfer")
def create_tool_transfer(tool_id: int = Form(...), to_site_id: int = Form(...), comment: str = Form(""), date: datetime = Form(...), db: Session = Depends(get_db)):
    crud_tr.create_tool_transfer(db=db, tool_id=tool_id, to_site_id=to_site_id, comment=comment, date=date)
    return RedirectResponse("/", status_code=303)

# --- Страница логина ---
@router.get("/login", response_class=HTMLResponse)
def login_page(
    request: Request,
    db: Session = Depends(get_db),
    current_user: Annotated[User | None, Depends(get_optional_user)] = None
):
    next_url = request.query_params.get("next", "/")
    if current_user:
        return RedirectResponse(next_url)
    return templates.TemplateResponse("login.html", {
        "request": request,
        "next": next_url
    })

# --- Регистрация ---
@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})
