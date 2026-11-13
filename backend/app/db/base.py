"""Declarative base, shared column types and mixins."""

import uuid
from datetime import datetime
from decimal import Decimal
from enum import Enum as PyEnum
from typing import Annotated

from sqlalchemy import DateTime, Enum, ForeignKey, MetaData, Numeric, func, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column

# Deterministic constraint names: required for clean Alembic migrations.
NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_N_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

# Reusable column types --------------------------------------------------
Latitude = Annotated[Decimal, mapped_column(Numeric(9, 6))]
Longitude = Annotated[Decimal, mapped_column(Numeric(9, 6))]
Quantity = Annotated[Decimal, mapped_column(Numeric(14, 3))]


def pg_enum(enum_cls: type[PyEnum], name: str) -> Enum:
    """Native PostgreSQL ENUM storing the Python enum *values* (lower-case)."""
    return Enum(
        enum_cls,
        name=name,
        values_callable=lambda members: [member.value for member in members],
        validate_strings=True,
    )


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=NAMING_CONVENTION)


class UUIDPrimaryKeyMixin:
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
        sort_order=-100,
    )


class CreatedAtMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), sort_order=100
    )


class TimestampMixin(CreatedAtMixin):
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
        sort_order=101,
    )


class OrganizationScopedMixin:
    """Every business record belongs to exactly one organisation (tenant).

    No standalone index here: each scoped table declares a unique constraint
    or composite index whose leading column is `organization_id`, which
    PostgreSQL already uses for tenant filtering.
    """

    @declared_attr
    def organization_id(cls) -> Mapped[uuid.UUID]:
        return mapped_column(
            UUID(as_uuid=True),
            ForeignKey("organizations.id", ondelete="CASCADE"),
            nullable=False,
            sort_order=-90,
        )
