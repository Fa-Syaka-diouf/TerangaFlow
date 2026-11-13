"""Physical sites: warehouses (stock holders) and distribution points (destinations)."""

from decimal import Decimal

from sqlalchemy import Boolean, CheckConstraint, Integer, Numeric, String, UniqueConstraint, true
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import (
    Base,
    Latitude,
    Longitude,
    OrganizationScopedMixin,
    TimestampMixin,
    UUIDPrimaryKeyMixin,
    pg_enum,
)
from app.models.enums import DistributionPointType


def _coordinate_checks() -> tuple[CheckConstraint, CheckConstraint]:
    """New constraint objects per table (SQLAlchemy constraints cannot be shared)."""
    return (
        CheckConstraint("latitude BETWEEN -90 AND 90", name="latitude_range"),
        CheckConstraint("longitude BETWEEN -180 AND 180", name="longitude_range"),
    )


class Warehouse(UUIDPrimaryKeyMixin, TimestampMixin, OrganizationScopedMixin, Base):
    __tablename__ = "warehouses"
    __table_args__ = (
        UniqueConstraint("organization_id", "code"),
        CheckConstraint("capacity_m3 IS NULL OR capacity_m3 > 0", name="capacity_positive"),
        *_coordinate_checks(),
    )

    code: Mapped[str] = mapped_column(String(32), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    region: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    address: Mapped[str | None] = mapped_column(String(300))
    latitude: Mapped[Latitude] = mapped_column(nullable=False)
    longitude: Mapped[Longitude] = mapped_column(nullable=False)
    capacity_m3: Mapped[Decimal | None] = mapped_column(Numeric(10, 2))
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=true())


class DistributionPoint(UUIDPrimaryKeyMixin, TimestampMixin, OrganizationScopedMixin, Base):
    __tablename__ = "distribution_points"
    __table_args__ = (
        UniqueConstraint("organization_id", "code"),
        CheckConstraint(
            "beneficiaries_count IS NULL OR beneficiaries_count >= 0",
            name="beneficiaries_non_negative",
        ),
        *_coordinate_checks(),
    )

    code: Mapped[str] = mapped_column(String(32), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    point_type: Mapped[DistributionPointType] = mapped_column(
        pg_enum(DistributionPointType, "distribution_point_type"), nullable=False
    )
    region: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    latitude: Mapped[Latitude] = mapped_column(nullable=False)
    longitude: Mapped[Longitude] = mapped_column(nullable=False)
    beneficiaries_count: Mapped[int | None] = mapped_column(Integer)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=true())
