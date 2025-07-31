from fastapi import APIRouter, Depends, Form, Body, HTTPException
from starlette.responses import RedirectResponse
from sqlalchemy.orm import Session
from datetime import datetime, date

from app.database.db import get_db
from app.schemas import schemas
from app.schemas.schemas import SiteCreate, SiteUpdate  # ← добавлено

from app.api.auth import get_current_user
from app.models.models import User
from pydantic import BaseModel

import app.crud.site      as crud_site
import app.crud.subgroups as crud_sg
import app.crud.expense   as crud_exp
import app.crud.salary    as crud_sal
import app.crud.worker    as crud_w
import app.crud.tool      as crud_tool
import app.crud.tool_transfer as crud_tr

router = APIRouter()

class PurchaseIn(BaseModel):
    amount: float
    site_id: int | None = None
    comment: str = ""
    form_date: str

# --- Объекты ---
@router.post("/api/sites", name="form.create_site")
def create_site(
    name: str = Form(...),
    address: str = Form(""),
    subgroup_id: int | None = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # ← добавить
):
    site = SiteCreate(name=name, address=address, subgroup_id=subgroup_id)
    crud_site.create_site(db, site, current_user.id)  # ← передаём user_id
    return RedirectResponse("/sites", status_code=303)

@router.post("/api/sites/{site_id}/archive", name="form.archive_site")
def archive_site(site_id: int, db: Session = Depends(get_db)):
    crud_site.archive_site(db, site_id)
    return RedirectResponse("/sites", status_code=303)

@router.post("/api/sites/{site_id}/restore", name="form.restore_site")
def restore_site(site_id: int, db: Session = Depends(get_db)):
    crud_site.restore_site(db, site_id)
    return RedirectResponse("/sites/archive", status_code=303)

@router.post("/api/sites/{site_id}/delete", name="form.delete_site")
def delete_site(site_id: int, db: Session = Depends(get_db)):
    crud_site.delete_site(db, site_id)
    return RedirectResponse("/sites", status_code=303)


# --- Подгруппы ---
@router.post("/api/subgroups", name="form.create_subgroup")
def create_subgroup(name: str = Form(...), db: Session = Depends(get_db)):
    crud_sg.create_subgroup(db, name)
    return RedirectResponse("/sites", status_code=303)

@router.post("/api/subgroups/{sg_id}")
def rename_subgroup(sg_id: int, name: str = Form(...), db: Session = Depends(get_db)):
    crud_sg.update_subgroup(db, sg_id, name)
    return RedirectResponse("/sites", status_code=303)

@router.post("/api/subgroups/{sg_id}/delete")
def delete_subgroup(sg_id: int, db: Session = Depends(get_db)):
    crud_sg.delete_subgroup(db, sg_id)
    return RedirectResponse("/sites", status_code=303)


# --- Закупка ---
@router.post("/api/expenses", name="form.create_expense")
def create_expense(
    purchase: PurchaseIn = Body(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    parsed_date = datetime.strptime(purchase.form_date, "%Y-%m-%d").date()

    crud_exp.create_expense(
        db=db,
        amount=purchase.amount,
        site_id=purchase.site_id,
        comment=purchase.comment,
        date=parsed_date,
        user_id=current_user.id
    )

    return {"ok": True}


# --- Зарплаты ---
@router.post("/api/salaries", name="form.create_salary")
def create_salary(
    amount: float = Form(...),
    worker_id: int = Form(...),
    site_id: int | None = Form(None),
    comment: str = Form(""),
    form_date: str = Form(...),
    db: Session = Depends(get_db)
):
    if isinstance(form_date, str):
        parsed_date = datetime.strptime(form_date, "%Y-%m-%d").date()
    else:
        parsed_date = datetime.today().date()

    salary_data = schemas.SalaryCreate(
    amount=amount,
    worker_id=worker_id,
    site_id=site_id,
    comment=comment,
    date=parsed_date
)
    crud_sal.create_salary(db=db, salary=salary_data)

    return RedirectResponse("/", status_code=303)



# --- Сотрудники ---
@router.post("/api/workers")
def create_worker(worker: schemas.WorkerCreate = Body(...), db: Session = Depends(get_db)):
    new_worker = crud_w.create_worker(db, worker)
    return new_worker  # возвращаем JSON (id, name, phone...)

@router.post("/api/workers/{id}")
def update_worker(id: int,
                  name: str = Form(...),
                  phone: str = Form(""),
                  db: Session = Depends(get_db)):
    crud_w.update_worker(db, id, schemas.WorkerUpdate(name=name, phone=phone))
    return RedirectResponse(f"/workers/{id}", status_code=303)

@router.post("/api/workers/{id}/archive")
def archive_worker(id: int, db: Session = Depends(get_db)):
    crud_w.archive_worker(db, id)
    return RedirectResponse("/workers", status_code=303)

@router.post("/api/workers/{id}/restore")
def restore_worker(id: int, db: Session = Depends(get_db)):
    crud_w.restore_worker(db, id)
    return RedirectResponse("/workers", status_code=303)

@router.post("/api/workers/{id}/delete")
def delete_worker(id: int, db: Session = Depends(get_db)):
    crud_w.delete_worker(db, id)
    return RedirectResponse("/workers", status_code=303)

# --- Инструменты ---
@router.post("/api/tools")
def create_tool(name: str = Form(...),
                price: float | None = Form(None),
                site_id: int | None = Form(None),
                db: Session = Depends(get_db)):
    crud_tool.create_tool(db, schemas.ToolCreate(
        name=name, price=price, site_id=site_id
    ))
    return RedirectResponse("/tools", status_code=303)

@router.post("/api/tools/{id}/delete")
def delete_tool(id: int, db: Session = Depends(get_db)):
    crud_tool.delete_tool(db, id)
    return RedirectResponse("/tools", status_code=303)


# --- Перемещения инструментов ---
@router.post("/api/tool-transfer")
def transfer_tool(tool_id: int = Form(...),
                  from_site_id: int | None = Form(None),
                  to_site_id: int | None = Form(None),
                  date_value: date = Form(None),
                  db: Session = Depends(get_db)):
    crud_tr.create_tool_transfer(db, schemas.ToolTransferCreate(
        tool_id=tool_id,
        from_site_id=from_site_id,
        to_site_id=to_site_id,
        comment="",
        date_value=date_value or date.today()
    ))
    return RedirectResponse("/warehouse", status_code=303)

@router.post("/api/tool-transfer/{id}/delete")
def delete_transfer(id: int, db: Session = Depends(get_db)):
    crud_tr.delete_tool_transfer(db, id)
    return RedirectResponse("/warehouse", status_code=303)

# --- Архивирование ---
@router.post("/api/sites/{site_id}/archive", name="form.archive_site")
def archive_site(site_id: int, db: Session = Depends(get_db)):
    crud_site.archive_site(db, site_id)
    return RedirectResponse("/sites", status_code=303)

# --- Редактирование объекта ---
@router.post("/api/sites/{site_id}", name="form.update_site")
def update_site(site_id: int,
                name: str = Form(...),
                address: str = Form(""),
                subgroup_id: int | None = Form(None),
                db: Session = Depends(get_db)):
    site_data = SiteCreate(name=name, address=address, subgroup_id=subgroup_id)
    crud_site.update_site(db, site_id, site_data)
    return RedirectResponse(f"/sites/{site_id}", status_code=303)

# --- Возврат из архива ---
@router.post("/api/sites/{site_id}/restore", name="form.restore_site")
def restore_site(site_id: int, db: Session = Depends(get_db)):
    site = crud_site.get_site(db, site_id)
    if not site:
        raise HTTPException(404, "Site not found")
    site.is_archived = False
    db.commit()
    return RedirectResponse("/sites/archive", status_code=303)

# --- Удаление объекта ---
@router.post("/api/sites/{site_id}/delete", name="form.delete_site")
def delete_site(site_id: int, db: Session = Depends(get_db)):
    crud_site.delete_site(db, site_id)
    return RedirectResponse("/sites", status_code=303)


