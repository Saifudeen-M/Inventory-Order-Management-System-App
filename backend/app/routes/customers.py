from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db


router = APIRouter(prefix="/customers", tags=["Customers"])


@router.get("/", response_model=List[schemas.CustomerRead])
def list_customers(db: Session = Depends(get_db)):
    return crud.list_customers(db)


@router.post("/", response_model=schemas.CustomerRead, status_code=status.HTTP_201_CREATED)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    return crud.create_customer(db, customer)


@router.get("/{customer_id}", response_model=schemas.CustomerRead)
def get_customer(customer_id: UUID, db: Session = Depends(get_db)):
    return crud.get_customer(db, customer_id)


@router.put("/{customer_id}", response_model=schemas.CustomerRead)
def update_customer(customer_id: UUID, customer: schemas.CustomerUpdate, db: Session = Depends(get_db)):
    return crud.update_customer(db, customer_id, customer)


@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(customer_id: UUID, db: Session = Depends(get_db)):
    crud.delete_customer(db, customer_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
