import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import (
    Base,
    OrganizationScopedMixin,
    TimestampMixin,
    UUIDPrimaryKeyMixin,
    pg_enum,
)
from app.models.enums import AlertSeverity, AlertStatus, RiskCategory


class RiskAlert(UUIDPrimaryKeyMixin, TimestampMixin, OrganizationScopedMixin, Base):
    """A risk that may disrupt operations, optionally linked to a delivery or site."""

    __tablename__ = "risk_alerts"
    __table_args__ = (
        UniqueConstraint("organization_id", "reference"),
        CheckConstraint(
            "(status = 'resolved') = (resolved_at IS NOT NULL)", name="resolved_at_matches_status"
        ),
        Index("ix_risk_alerts_organization_id_status_severity", "organization_id", "status", "severity"),
        Index("ix_risk_alerts_detected_at", "detected_at"),
    )

    reference: Mapped[str] = mapped_column(String(32), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    category: Mapped[RiskCategory] = mapped_column(
        pg_enum(RiskCategory, "risk_category"), nullable=False
    )
    severity: Mapped[AlertSeverity] = mapped_column(
        pg_enum(AlertSeverity, "alert_severity"), nullable=False
    )
    status: Mapped[AlertStatus] = mapped_column(
        pg_enum(AlertStatus, "alert_status"),
        nullable=False,
        server_default=AlertStatus.OPEN.value,
    )
    region: Mapped[str | None] = mapped_column(String(100))
    delivery_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("deliveries.id", ondelete="SET NULL"), index=True
    )
    warehouse_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("warehouses.id", ondelete="SET NULL"), index=True
    )
    distribution_point_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("distribution_points.id", ondelete="SET NULL"), index=True
    )
    vehicle_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("vehicles.id", ondelete="SET NULL"), index=True
    )
    detected_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
