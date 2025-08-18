# app/api/salary.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.db import get_db
import app.crud.salary as crud_sal
from app.api.auth import get_current_user
from app.models.models import User

router = APIRouter(prefix="/api/salaries", tags=["Salaries"])

@router.get("/")
def read_salaries(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud_sal.get_salaries(db, user_id=current_user.id)
