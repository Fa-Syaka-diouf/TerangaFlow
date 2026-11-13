"""ORM models. Importing this package registers every table on `Base.metadata`
(required by Alembic autogenerate)."""

from app.db.base import Base
from app.models.delivery import Delivery
from app.models.fleet import Vehicle
from app.models.inventory import InventoryItem, InventoryTransaction
from app.models.location import DistributionPoint, Warehouse
from app.models.organization import Organization
from app.models.risk_alert import RiskAlert

__all__ = [
    "Base",
    "Delivery",
    "DistributionPoint",
    "InventoryItem",
    "InventoryTransaction",
    "Organization",
    "RiskAlert",
    "Vehicle",
    "Warehouse",
]
