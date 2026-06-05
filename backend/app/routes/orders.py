from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db


router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get("/", response_model=List[schemas.OrderRead])
def list_orders(db: Session = Depends(get_db)):
    return crud.list_orders(db)


@router.post("/", response_model=schemas.OrderRead, status_code=status.HTTP_201_CREATED)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    return crud.create_order(db, order)


@router.get("/{order_id}", response_model=schemas.OrderRead)
def get_order(order_id: UUID, db: Session = Depends(get_db)):
    return crud.get_order(db, order_id)
