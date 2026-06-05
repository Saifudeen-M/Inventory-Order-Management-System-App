"""initial schema

Revision ID: 20260605_0001
Revises:
Create Date: 2026-06-05
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20260605_0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if not inspector.has_table("customers"):
        op.create_table(
            "customers",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("name", sa.String(length=120), nullable=False),
            sa.Column("email", sa.String(length=255), nullable=False),
            sa.Column("phone", sa.String(length=40), nullable=True),
            sa.Column("address", sa.Text(), nullable=True),
            sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
            sa.PrimaryKeyConstraint("id"),
        )
    existing_customer_indexes = {index["name"] for index in inspector.get_indexes("customers")}
    if op.f("ix_customers_email") not in existing_customer_indexes:
        op.create_index(op.f("ix_customers_email"), "customers", ["email"], unique=True)
    if op.f("ix_customers_id") not in existing_customer_indexes:
        op.create_index(op.f("ix_customers_id"), "customers", ["id"], unique=False)

    if not inspector.has_table("products"):
        op.create_table(
            "products",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("name", sa.String(length=120), nullable=False),
            sa.Column("sku", sa.String(length=60), nullable=False),
            sa.Column("description", sa.Text(), nullable=True),
            sa.Column("price", sa.Numeric(10, 2), nullable=False),
            sa.Column("stock_quantity", sa.Integer(), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
            sa.PrimaryKeyConstraint("id"),
        )
    existing_product_indexes = {index["name"] for index in inspector.get_indexes("products")}
    if op.f("ix_products_id") not in existing_product_indexes:
        op.create_index(op.f("ix_products_id"), "products", ["id"], unique=False)
    if op.f("ix_products_sku") not in existing_product_indexes:
        op.create_index(op.f("ix_products_sku"), "products", ["sku"], unique=True)

    if not inspector.has_table("orders"):
        op.create_table(
            "orders",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("customer_id", sa.Integer(), nullable=False),
            sa.Column("status", sa.String(length=40), nullable=False),
            sa.Column("total_amount", sa.Numeric(10, 2), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
            sa.ForeignKeyConstraint(["customer_id"], ["customers.id"], ondelete="CASCADE"),
            sa.PrimaryKeyConstraint("id"),
        )
    existing_order_indexes = {index["name"] for index in inspector.get_indexes("orders")}
    if op.f("ix_orders_id") not in existing_order_indexes:
        op.create_index(op.f("ix_orders_id"), "orders", ["id"], unique=False)

    if not inspector.has_table("order_items"):
        op.create_table(
            "order_items",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("order_id", sa.Integer(), nullable=False),
            sa.Column("product_id", sa.Integer(), nullable=False),
            sa.Column("quantity", sa.Integer(), nullable=False),
            sa.Column("unit_price", sa.Numeric(10, 2), nullable=False),
            sa.Column("line_total", sa.Numeric(10, 2), nullable=False),
            sa.ForeignKeyConstraint(["order_id"], ["orders.id"], ondelete="CASCADE"),
            sa.ForeignKeyConstraint(["product_id"], ["products.id"], ondelete="RESTRICT"),
            sa.PrimaryKeyConstraint("id"),
        )
    existing_order_item_indexes = {index["name"] for index in inspector.get_indexes("order_items")}
    if op.f("ix_order_items_id") not in existing_order_item_indexes:
        op.create_index(op.f("ix_order_items_id"), "order_items", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_order_items_id"), table_name="order_items")
    op.drop_table("order_items")
    op.drop_index(op.f("ix_orders_id"), table_name="orders")
    op.drop_table("orders")
    op.drop_index(op.f("ix_products_sku"), table_name="products")
    op.drop_index(op.f("ix_products_id"), table_name="products")
    op.drop_table("products")
    op.drop_index(op.f("ix_customers_id"), table_name="customers")
    op.drop_index(op.f("ix_customers_email"), table_name="customers")
    op.drop_table("customers")
