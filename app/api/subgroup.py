# app/api/subgroup.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.db import get_db
import app.crud.subgroups as crud
from app.api.auth import get_current_user
from app.models.models import User

router = APIRouter(prefix="/api/subgroups", tags=["Subgroups"])

@router.get("/")
def read_subgroups(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # отдаём только подгруппы текущего пользователя
    return crud.get_subgroups(db, user_id=current_user.id)
