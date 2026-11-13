import uuid
from decimal import Decimal

from sqlalchemy import CheckConstraint, ForeignKey, Index, Numeric, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import (
    Base,
    OrganizationScopedMixin,
    TimestampMixin,
    UUIDPrimaryKeyMixin,
    pg_enum,
)
from app.models.enums import VehicleStatus, VehicleType


class Vehicle(UUIDPrimaryKeyMixin, TimestampMixin, OrganizationScopedMixin, Base):
    __tablename__ = "vehicles"
    __table_args__ = (
        UniqueConstraint("organization_id", "registration_number"),
        CheckConstraint("capacity_kg > 0", name="capacity_positive"),
        Index("ix_vehicles_organization_id_status", "organization_id", "status"),
    )

    registration_number: Mapped[str] = mapped_column(String(32), nullable=False)
    label: Mapped[str] = mapped_column(String(100), nullable=False)
    vehicle_type: Mapped[VehicleType] = mapped_column(
        pg_enum(VehicleType, "vehicle_type"), nullable=False
    )
    status: Mapped[VehicleStatus] = mapped_column(
        pg_enum(VehicleStatus, "vehicle_status"),
        nullable=False,
        server_default=VehicleStatus.AVAILABLE.value,
    )
    capacity_kg: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    home_warehouse_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("warehouses.id", ondelete="SET NULL"), index=True
    )
    driver_name: Mapped[str | None] = mapped_column(String(150))
