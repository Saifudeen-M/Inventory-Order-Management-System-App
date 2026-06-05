"""sync existing tables

Revision ID: 20260605_0002
Revises: 20260605_0001
Create Date: 2026-06-05
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20260605_0002"
down_revision: Union[str, None] = "20260605_0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _column_names(table_name: str) -> set:
    inspector = sa.inspect(op.get_bind())
    return {column["name"] for column in inspector.get_columns(table_name)}


def _index_names(table_name: str) -> set:
    inspector = sa.inspect(op.get_bind())
    return {index["name"] for index in inspector.get_indexes(table_name)}


def _add_missing_column(table_name: str, column: sa.Column) -> None:
    if column.name not in _column_names(table_name):
        op.add_column(table_name, column)


def _create_missing_index(table_name: str, index_name: str, columns: list, unique: bool = False) -> None:
    if index_name not in _index_names(table_name):
        op.create_index(index_name, table_name, columns, unique=unique)


def upgrade() -> None:
    inspector = sa.inspect(op.get_bind())
    tables = set(inspector.get_table_names())

    if "products" in tables:
        _add_missing_column("products", sa.Column("description", sa.Text(), nullable=True))
        _add_missing_column("products", sa.Column("price", sa.Numeric(10, 2), nullable=False, server_default="0"))
        _add_missing_column("products", sa.Column("stock_quantity", sa.Integer(), nullable=False, server_default="0"))
        _add_missing_column(
            "products",
            sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        )
        _add_missing_column(
            "products",
            sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        )
        _create_missing_index("products", op.f("ix_products_id"), ["id"])
        _create_missing_index("products", op.f("ix_products_sku"), ["sku"], unique=True)

    if "customers" in tables:
        _add_missing_column("customers", sa.Column("phone", sa.String(length=40), nullable=True))
        _add_missing_column("customers", sa.Column("address", sa.Text(), nullable=True))
        _add_missing_column(
            "customers",
            sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        )
        _add_missing_column(
            "customers",
            sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        )
        _create_missing_index("customers", op.f("ix_customers_id"), ["id"])
        _create_missing_index("customers", op.f("ix_customers_email"), ["email"], unique=True)

    if "orders" in tables:
        _add_missing_column("orders", sa.Column("status", sa.String(length=40), nullable=False, server_default="placed"))
        _add_missing_column("orders", sa.Column("total_amount", sa.Numeric(10, 2), nullable=False, server_default="0"))
        _add_missing_column(
            "orders",
            sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        )
        _add_missing_column(
            "orders",
            sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        )
        _create_missing_index("orders", op.f("ix_orders_id"), ["id"])

    if "order_items" in tables:
        _add_missing_column("order_items", sa.Column("unit_price", sa.Numeric(10, 2), nullable=False, server_default="0"))
        _add_missing_column("order_items", sa.Column("line_total", sa.Numeric(10, 2), nullable=False, server_default="0"))
        _create_missing_index("order_items", op.f("ix_order_items_id"), ["id"])


def downgrade() -> None:
    pass
