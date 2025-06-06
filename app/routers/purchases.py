from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db import get_db
from app import crud, models, schemas  # Импортируем всё из app.schemas, включая Purchase и PurchaseCreate

router = APIRouter(prefix="/purchases", tags=["Purchases"])


@router.post("/", response_model=schemas.Purchase)
def create_purchase(purchase: schemas.PurchaseCreate, db: Session = Depends(get_db)):
    return crud.purchase.create(db=db, purchase=purchase)


@router.get("/", response_model=list[schemas.Purchase])
def read_purchases(db: Session = Depends(get_db)):
    return crud.purchase.get_all(db)


@router.get("/{purchase_id}", response_model=schemas.Purchase)
def read_purchase(purchase_id: int, db: Session = Depends(get_db)):
    db_purchase = crud.purchase.get(db, purchase_id)
    if db_purchase is None:
        raise HTTPException(status_code=404, detail="Purchase not found")
    return db_purchase


@router.put("/{purchase_id}", response_model=schemas.Purchase)
def update_purchase(purchase_id: int, updated: schemas.PurchaseCreate, db: Session = Depends(get_db)):
    return crud.purchase.update(db, purchase_id, updated)


@router.delete("/{purchase_id}")
def delete_purchase(purchase_id: int, db: Session = Depends(get_db)):
    crud.purchase.delete(db, purchase_id)
    return {"message": "Purchase deleted"}
