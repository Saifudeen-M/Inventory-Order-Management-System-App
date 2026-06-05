from decimal import Decimal
from typing import Dict, List

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

from app import models, schemas


def list_products(db: Session) -> List[models.Product]:
    return list(db.scalars(select(models.Product).order_by(models.Product.id)))


def create_product(db: Session, product_in: schemas.ProductCreate) -> models.Product:
    product = models.Product(**product_in.model_dump())
    db.add(product)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status.HTTP_409_CONFLICT, "Product SKU already exists") from exc
    db.refresh(product)
    return product


def get_product(db: Session, product_id: int) -> models.Product:
    product = db.get(models.Product, product_id)
    if not product:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Product not found")
    return product


def update_product(db: Session, product_id: int, product_in: schemas.ProductUpdate) -> models.Product:
    product = get_product(db, product_id)
    for field, value in product_in.model_dump(exclude_unset=True).items():
        setattr(product, field, value)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status.HTTP_409_CONFLICT, "Product SKU already exists") from exc
    db.refresh(product)
    return product


def delete_product(db: Session, product_id: int) -> None:
    product = get_product(db, product_id)
    db.delete(product)
    db.commit()


def list_customers(db: Session) -> List[models.Customer]:
    return list(db.scalars(select(models.Customer).order_by(models.Customer.id)))


def create_customer(db: Session, customer_in: schemas.CustomerCreate) -> models.Customer:
    customer = models.Customer(**customer_in.model_dump())
    db.add(customer)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status.HTTP_409_CONFLICT, "Customer email already exists") from exc
    db.refresh(customer)
    return customer


def get_customer(db: Session, customer_id: int) -> models.Customer:
    customer = db.get(models.Customer, customer_id)
    if not customer:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Customer not found")
    return customer


def update_customer(db: Session, customer_id: int, customer_in: schemas.CustomerUpdate) -> models.Customer:
    customer = get_customer(db, customer_id)
    for field, value in customer_in.model_dump(exclude_unset=True).items():
        setattr(customer, field, value)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status.HTTP_409_CONFLICT, "Customer email already exists") from exc
    db.refresh(customer)
    return customer


def delete_customer(db: Session, customer_id: int) -> None:
    customer = get_customer(db, customer_id)
    db.delete(customer)
    db.commit()


def list_orders(db: Session) -> List[models.Order]:
    stmt = (
        select(models.Order)
        .options(selectinload(models.Order.customer), selectinload(models.Order.items))
        .order_by(models.Order.id.desc())
    )
    return list(db.scalars(stmt))


def get_order(db: Session, order_id: int) -> models.Order:
    stmt = (
        select(models.Order)
        .where(models.Order.id == order_id)
        .options(selectinload(models.Order.customer), selectinload(models.Order.items))
    )
    order = db.scalar(stmt)
    if not order:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Order not found")
    return order


def create_order(db: Session, order_in: schemas.OrderCreate) -> models.Order:
    customer = db.get(models.Customer, order_in.customer_id)
    if not customer:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Customer not found")

    requested: Dict[int, int] = {}
    for item in order_in.items:
        requested[item.product_id] = requested.get(item.product_id, 0) + item.quantity

    products = list(
        db.scalars(select(models.Product).where(models.Product.id.in_(requested.keys())).with_for_update())
    )
    product_by_id = {product.id: product for product in products}
    missing_ids = sorted(set(requested) - set(product_by_id))
    if missing_ids:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Products not found: {missing_ids}")

    for product_id, quantity in requested.items():
        product = product_by_id[product_id]
        if product.stock_quantity < quantity:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                f"Insufficient stock for SKU {product.sku}. Available: {product.stock_quantity}, requested: {quantity}",
            )

    order = models.Order(customer_id=customer.id, status="placed", total_amount=Decimal("0.00"))
    db.add(order)
    total = Decimal("0.00")
    for product_id, quantity in requested.items():
        product = product_by_id[product_id]
        line_total = Decimal(product.price) * quantity
        product.stock_quantity -= quantity
        total += line_total
        order.items.append(
            models.OrderItem(
                product_id=product.id,
                quantity=quantity,
                unit_price=product.price,
                line_total=line_total,
            )
        )
    order.total_amount = total
    db.commit()
    return get_order(db, order.id)
