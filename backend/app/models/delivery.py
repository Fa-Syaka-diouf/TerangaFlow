import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import (
    Base,
    OrganizationScopedMixin,
    TimestampMixin,
    UUIDPrimaryKeyMixin,
    pg_enum,
)
from app.models.enums import DeliveryPriority, DeliveryStatus


class Delivery(UUIDPrimaryKeyMixin, TimestampMixin, OrganizationScopedMixin, Base):
    """A shipment from a warehouse to a distribution point."""

    __tablename__ = "deliveries"
    __table_args__ = (
        UniqueConstraint("organization_id", "reference"),
        CheckConstraint(
            "planned_arrival_at >= planned_departure_at", name="planned_window_valid"
        ),
        CheckConstraint(
            "actual_arrival_at IS NULL OR actual_departure_at IS NULL"
            " OR actual_arrival_at >= actual_departure_at",
            name="actual_window_valid",
        ),
        CheckConstraint(
            "status <> 'delivered' OR actual_arrival_at IS NOT NULL",
            name="delivered_has_arrival",
        ),
        CheckConstraint("cargo_weight_kg IS NULL OR cargo_weight_kg > 0", name="weight_positive"),
        Index("ix_deliveries_organization_id_status", "organization_id", "status"),
        Index("ix_deliveries_planned_departure_at", "planned_departure_at"),
    )

    reference: Mapped[str] = mapped_column(String(32), nullable=False)
    origin_warehouse_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("warehouses.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    destination_point_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("distribution_points.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    vehicle_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("vehicles.id", ondelete="SET NULL"), index=True
    )
    status: Mapped[DeliveryStatus] = mapped_column(
        pg_enum(DeliveryStatus, "delivery_status"),
        nullable=False,
        server_default=DeliveryStatus.PLANNED.value,
    )
    priority: Mapped[DeliveryPriority] = mapped_column(
        pg_enum(DeliveryPriority, "delivery_priority"),
        nullable=False,
        server_default=DeliveryPriority.NORMAL.value,
    )
    cargo_description: Mapped[str] = mapped_column(String(300), nullable=False)
    cargo_weight_kg: Mapped[Decimal | None] = mapped_column(Numeric(10, 2))
    planned_departure_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    planned_arrival_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    actual_departure_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    actual_arrival_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    notes: Mapped[str | None] = mapped_column(Text)
