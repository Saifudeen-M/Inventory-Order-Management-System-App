from datetime import datetime
from decimal import Decimal
from uuid import UUID
from typing import List, Optional

from pydantic import (
    AliasChoices,
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
)


# =========================
# Product Schemas
# =========================

class ProductBase(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    sku: str = Field(min_length=1, max_length=60)
    description: Optional[str] = None
    price: Decimal = Field(gt=0, max_digits=10, decimal_places=2)

    stock_quantity: int = Field(
        validation_alias=AliasChoices(
            "stock_quantity",
            "stock",
            "quantity"
        ),
        ge=0
    )

    model_config = ConfigDict(populate_by_name=True)


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=120)
    sku: Optional[str] = Field(default=None, min_length=1, max_length=60)
    description: Optional[str] = None
    price: Optional[Decimal] = Field(
        default=None,
        gt=0,
        max_digits=10,
        decimal_places=2
    )

    stock_quantity: Optional[int] = Field(
        default=None,
        validation_alias=AliasChoices(
            "stock_quantity",
            "stock",
            "quantity"
        ),
        ge=0
    )

    model_config = ConfigDict(populate_by_name=True)


class ProductRead(ProductBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# =========================
# Customer Schemas
# =========================

class CustomerBase(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    email: EmailStr
    phone: Optional[str] = Field(default=None, max_length=40)
    address: Optional[str] = None


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=120)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(default=None, max_length=40)
    address: Optional[str] = None


class CustomerRead(CustomerBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# =========================
# Order Item Schemas
# =========================

class OrderItemCreate(BaseModel):
    product_id: UUID
    quantity: int = Field(gt=0)


class OrderItemRead(BaseModel):
    id: UUID
    product_id: UUID
    quantity: int
    unit_price: Decimal
    line_total: Decimal

    model_config = ConfigDict(from_attributes=True)


# =========================
# Order Schemas
# =========================

class OrderCreate(BaseModel):
    customer_id: UUID
    items: List[OrderItemCreate] = Field(min_length=1)


class OrderRead(BaseModel):
    id: UUID
    customer_id: UUID
    status: str
    total_amount: Decimal
    created_at: datetime
    updated_at: datetime

    items: List[OrderItemRead] = []

    model_config = ConfigDict(from_attributes=True)


# =========================
# Detailed Order Response
# =========================

class OrderDetailRead(OrderRead):
    customer: CustomerRead
    items: List[OrderItemRead]