"""Stock lines per warehouse and the append-only ledger of their movements."""

import uuid
from datetime import date, datetime

from sqlalchemy import (
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    Index,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import (
    Base,
    CreatedAtMixin,
    OrganizationScopedMixin,
    Quantity,
    TimestampMixin,
    UUIDPrimaryKeyMixin,
    pg_enum,
)
from app.models.enums import InventoryTransactionType, ItemCategory


class InventoryItem(UUIDPrimaryKeyMixin, TimestampMixin, OrganizationScopedMixin, Base):
    """Current stock of one article (SKU) in one warehouse.

    `quantity` is a denormalised balance; the history lives in
    `inventory_transactions`.
    """

    __tablename__ = "inventory_items"
    __table_args__ = (
        UniqueConstraint("warehouse_id", "sku"),
        CheckConstraint("quantity >= 0", name="quantity_non_negative"),
        CheckConstraint("reorder_level >= 0", name="reorder_level_non_negative"),
        Index("ix_inventory_items_organization_id_category", "organization_id", "category"),
    )

    warehouse_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("warehouses.id", ondelete="CASCADE"), nullable=False
    )
    sku: Mapped[str] = mapped_column(String(64), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    category: Mapped[ItemCategory] = mapped_column(
        pg_enum(ItemCategory, "item_category"), nullable=False
    )
    unit: Mapped[str] = mapped_column(String(32), nullable=False)
    quantity: Mapped[Quantity] = mapped_column(nullable=False, server_default="0")
    reorder_level: Mapped[Quantity] = mapped_column(nullable=False, server_default="0")
    expiry_date: Mapped[date | None] = mapped_column(Date)


class InventoryTransaction(UUIDPrimaryKeyMixin, CreatedAtMixin, OrganizationScopedMixin, Base):
    """Immutable stock movement. `quantity_change` is signed (+ in, − out)."""

    __tablename__ = "inventory_transactions"
    __table_args__ = (
        UniqueConstraint("organization_id", "reference"),
        CheckConstraint("quantity_change <> 0", name="quantity_change_non_zero"),
        CheckConstraint(
            "(transaction_type = 'inbound' AND quantity_change > 0)"
            " OR (transaction_type IN ('outbound', 'loss') AND quantity_change < 0)"
            " OR transaction_type = 'adjustment'",
            name="quantity_sign_matches_type",
        ),
        Index(
            "ix_inventory_transactions_item_occurred_at", "inventory_item_id", "occurred_at"
        ),
    )

    inventory_item_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("inventory_items.id", ondelete="CASCADE"), nullable=False
    )
    delivery_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("deliveries.id", ondelete="SET NULL"), index=True
    )
    reference: Mapped[str] = mapped_column(String(64), nullable=False)
    transaction_type: Mapped[InventoryTransactionType] = mapped_column(
        pg_enum(InventoryTransactionType, "inventory_transaction_type"), nullable=False
    )
    quantity_change: Mapped[Quantity] = mapped_column(nullable=False)
    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    note: Mapped[str | None] = mapped_column(Text)
