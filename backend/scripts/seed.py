"""Load the SIMULATED demonstration dataset (see `scripts/seed_data.py`).

Usage (from `backend/`, after `alembic upgrade head`):

    python -m scripts.seed

Idempotent: every row is upserted on its natural key
(`INSERT ... ON CONFLICT DO UPDATE`), so re-running the script refreshes the
data instead of duplicating it. All writes happen in a single transaction.
"""

import logging
import sys
from collections import defaultdict
from collections.abc import Iterable, Mapping, Sequence
from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.base import Base
from app.db.session import build_engine
from app.models import (
    Delivery,
    DistributionPoint,
    InventoryItem,
    InventoryTransaction,
    Organization,
    RiskAlert,
    Vehicle,
    Warehouse,
)
from app.models.enums import AlertStatus, DeliveryStatus, InventoryTransactionType
from scripts import seed_data as data

logger = logging.getLogger("seed")

# Movements dated before this offset (hours) are the initial stock receptions.
INITIAL_RECEIPT_OFFSET_H = -720  # 30 days before the anchor


def upsert(
    session: Session,
    model: type[Base],
    rows: Sequence[Mapping[str, Any]],
    conflict_columns: Sequence[str],
) -> dict[tuple[Any, ...], UUID]:
    """Insert or update `rows`; return {natural key tuple: id}."""
    if not rows:
        return {}
    stmt = insert(model).values(list(rows))
    updatable = {
        column: stmt.excluded[column] for column in rows[0] if column not in conflict_columns
    }
    if "updated_at" in model.__table__.c:
        updatable["updated_at"] = func.now()
    stmt = stmt.on_conflict_do_update(index_elements=list(conflict_columns), set_=updatable)
    key_columns = [model.__table__.c[column] for column in conflict_columns]
    result = session.execute(stmt.returning(model.__table__.c.id, *key_columns))
    return {tuple(row[1:]): row[0] for row in result}


def by_code(mapping: Mapping[tuple[Any, ...], UUID]) -> dict[str, UUID]:
    """Reduce {(organization_id, code): id} to {code: id}."""
    return {key[-1]: value for key, value in mapping.items()}


def seed(session: Session, anchor: datetime) -> dict[str, int]:
    def at(offset_hours: int | None) -> datetime | None:
        return None if offset_hours is None else anchor + timedelta(hours=offset_hours)

    # --- Organisation --------------------------------------------------------
    org_id = upsert(session, Organization, [data.ORGANIZATION], ["slug"])[(data.ORGANIZATION["slug"],)]
    scoped = {"organization_id": org_id}

    # --- Sites -----------------------------------------------------------------
    warehouses = by_code(
        upsert(
            session,
            Warehouse,
            [
                {**scoped, "code": code, "name": name, "region": region, "city": city, "address": address,
                 "latitude": lat, "longitude": lon, "capacity_m3": capacity}
                for code, name, region, city, address, lat, lon, capacity in data.WAREHOUSES
            ],
            ["organization_id", "code"],
        )
    )
    points = by_code(
        upsert(
            session,
            DistributionPoint,
            [
                {**scoped, "code": code, "name": name, "point_type": point_type, "region": region,
                 "city": city, "latitude": lat, "longitude": lon, "beneficiaries_count": beneficiaries}
                for code, name, point_type, region, city, lat, lon, beneficiaries in data.DISTRIBUTION_POINTS
            ],
            ["organization_id", "code"],
        )
    )

    # --- Fleet -----------------------------------------------------------------
    vehicles = by_code(
        upsert(
            session,
            Vehicle,
            [
                {**scoped, "registration_number": plate, "label": label, "vehicle_type": vehicle_type,
                 "status": status, "capacity_kg": capacity, "home_warehouse_id": warehouses[home],
                 "driver_name": driver}
                for plate, label, vehicle_type, status, capacity, home, driver in data.VEHICLES
            ],
            ["organization_id", "registration_number"],
        )
    )

    # --- Deliveries ------------------------------------------------------------
    deliveries = by_code(
        upsert(
            session,
            Delivery,
            [
                {**scoped, "reference": d.reference, "origin_warehouse_id": warehouses[d.origin],
                 "destination_point_id": points[d.destination],
                 "vehicle_id": vehicles[d.vehicle] if d.vehicle else None,
                 "status": d.status, "priority": d.priority, "cargo_description": d.cargo,
                 "cargo_weight_kg": d.weight_kg,
                 "planned_departure_at": at(d.planned_departure_h),
                 "planned_arrival_at": at(d.planned_arrival_h),
                 "actual_departure_at": at(d.actual_departure_h),
                 "actual_arrival_at": at(d.actual_arrival_h), "notes": d.notes}
                for d in data.DELIVERIES
            ],
            ["organization_id", "reference"],
        )
    )

    # --- Inventory: balances are derived from the movement ledger --------------
    outbound: dict[tuple[str, str], list[tuple[data.DeliverySeed, int]]] = defaultdict(list)
    for d in data.DELIVERIES:
        if d.actual_departure_h is not None and d.status != DeliveryStatus.CANCELLED:
            for sku, quantity in d.items:
                outbound[(d.origin, sku)].append((d, quantity))

    item_rows = []
    for (warehouse_code, sku), quantity in data.STOCK.items():
        name, category, unit, reorder_level = data.CATALOG[sku]
        item_rows.append(
            {**scoped, "warehouse_id": warehouses[warehouse_code], "sku": sku, "name": name,
             "category": category, "unit": unit, "quantity": quantity, "reorder_level": reorder_level}
        )
    items_by_key = upsert(session, InventoryItem, item_rows, ["warehouse_id", "sku"])
    warehouse_code_by_id = {value: key for key, value in warehouses.items()}
    items = {(warehouse_code_by_id[wh_id], sku): item_id for (wh_id, sku), item_id in items_by_key.items()}

    transaction_rows = []
    for (warehouse_code, sku), current in data.STOCK.items():
        item_id = items[(warehouse_code, sku)]
        shipped = outbound.get((warehouse_code, sku), [])
        transaction_rows.append(
            {**scoped, "inventory_item_id": item_id, "delivery_id": None,
             "reference": f"RCV-{warehouse_code}-{sku}",
             "transaction_type": InventoryTransactionType.INBOUND,
             "quantity_change": current + sum(quantity for _, quantity in shipped),
             "occurred_at": at(INITIAL_RECEIPT_OFFSET_H),
             "note": "Réception initiale du stock (simulé)."}
        )
        for delivery, quantity in shipped:
            transaction_rows.append(
                {**scoped, "inventory_item_id": item_id, "delivery_id": deliveries[delivery.reference],
                 "reference": f"OUT-{delivery.reference}-{sku}",
                 "transaction_type": InventoryTransactionType.OUTBOUND,
                 "quantity_change": -quantity, "occurred_at": at(delivery.actual_departure_h),
                 "note": f"Expédition {delivery.reference} (simulé)."}
            )
    upsert(session, InventoryTransaction, transaction_rows, ["organization_id", "reference"])

    # --- Risk alerts -------------------------------------------------------------
    upsert(
        session,
        RiskAlert,
        [
            {**scoped, "reference": a.reference, "title": a.title, "description": a.description,
             "category": a.category, "severity": a.severity, "status": a.status, "region": a.region,
             "delivery_id": deliveries[a.delivery] if a.delivery else None,
             "warehouse_id": warehouses[a.warehouse] if a.warehouse else None,
             "distribution_point_id": points[a.distribution_point] if a.distribution_point else None,
             "vehicle_id": vehicles[a.vehicle] if a.vehicle else None,
             "detected_at": at(a.detected_h),
             "resolved_at": at(a.resolved_h) if a.status == AlertStatus.RESOLVED else None}
            for a in data.ALERTS
        ],
        ["organization_id", "reference"],
    )

    return count_rows(session, org_id)


def count_rows(session: Session, org_id: UUID) -> dict[str, int]:
    models: Iterable[type[Base]] = (
        Warehouse, DistributionPoint, InventoryItem, InventoryTransaction, Vehicle, Delivery, RiskAlert,
    )
    counts = {"organizations": session.scalar(select(func.count()).select_from(Organization)) or 0}
    for model in models:
        table = model.__table__
        counts[table.name] = session.scalar(
            select(func.count()).select_from(table).where(table.c.organization_id == org_id)
        ) or 0
    return counts


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    settings = get_settings()
    if not settings.is_database_configured:
        logger.error("DATABASE_URL is not set. Copy backend/.env.example to backend/.env and fill it in.")
        return 1

    # Anchor: today 08:00 UTC — relative timestamps stay identical for re-runs on the same day.
    anchor = datetime.now(UTC).replace(hour=8, minute=0, second=0, microsecond=0)

    engine = build_engine(settings, null_pool=True)
    try:
        with Session(engine) as session, session.begin():
            counts = seed(session, anchor)
    finally:
        engine.dispose()

    logger.info("Demo data loaded (SIMULATED) - anchor %s", anchor.isoformat())
    for table, count in counts.items():
        logger.info("  %-24s %d", table, count)
    return 0


if __name__ == "__main__":
    sys.exit(main())
