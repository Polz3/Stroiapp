# app/api/expense.py
from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from datetime import datetime

from app.database.db import get_db
import app.crud.expense as crud_exp
import app.crud.salary as crud_sal
from app.api.auth import get_current_user
from app.models.models import User

router = APIRouter(prefix="/api/expenses", tags=["Expenses"])

# --- CREATE (закупка) вызывается с главной через JSON ---
@router.post("")
@router.post("/")
def create_expense(
    purchase: dict = Body(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # ожидаем payload: {amount, site_id, comment, form_date}
    amount = float(purchase.get("amount", 0))
    site_id = purchase.get("site_id")
    site_id = int(site_id) if site_id not in (None, "", "null") else None
    comment = purchase.get("comment", "") or ""
    form_date = purchase.get("form_date") or datetime.today().strftime("%Y-%m-%d")
    parsed_date = datetime.strptime(form_date, "%Y-%m-%d").date()

    crud_exp.create_expense(
        db=db,
        amount=amount,
        site_id=site_id,
        comment=comment,
        date=parsed_date,
        user_id=current_user.id,
        type="purchase",
        worker_id=None
    )
    return {"ok": True}

# --- READ (единый список для страницы «Расходы») ---
@router.get("")
@router.get("/")
def list_expenses(
    site_id: int | None = None,
    type: str = "",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # закупки
    expenses = crud_exp.get_expenses(db, user_id=current_user.id)
    # зарплаты
    salaries = crud_sal.get_salaries(db, user_id=current_user.id)

    rows: list[dict] = []

    # нормализуем закупки
    for e in expenses:
        rows.append({
            "id": e.id,
            "amount": e.amount,
            "type": (e.type or "purchase"),
            "comment": e.comment or "",
            "date": e.date.isoformat(),
            "site_id": e.site_id,
            "worker_id": e.worker_id,
            "site_name": e.site.name if getattr(e, "site", None) else None,
            "worker_name": e.worker.name if getattr(e, "worker", None) else None
        })

    # нормализуем зарплаты как «расходы» типа salary
    for s in salaries:
        rows.append({
            "id": s.id,
            "amount": s.amount,
            "type": "salary",
            "comment": s.comment or "Зарплата",
            "date": s.date.isoformat(),
            "site_id": s.site_id,
            "worker_id": s.worker_id,
            "site_name": s.site.name if getattr(s, "site", None) else None,
            "worker_name": s.worker.name if getattr(s, "worker", None) else None
        })

    # необязательные фильтры (как на фронте)
    if site_id is not None:
        rows = [r for r in rows if r["site_id"] == site_id]
    if type in ("purchase", "salary"):
        rows = [r for r in rows if r["type"] == type]

    # сортировка по дате и id (новее выше)
    rows.sort(key=lambda r: (r["date"], r["id"]), reverse=True)
    return rows
