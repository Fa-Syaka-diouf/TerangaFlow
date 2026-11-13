"""Business enumerations, stored as native PostgreSQL ENUM types.

Values are lower-case snake_case; they are mirrored by the frontend
(`frontend/src/types/domain.ts`).
"""

from enum import StrEnum


class DistributionPointType(StrEnum):
    COMMUNITY_CENTER = "community_center"
    HEALTH_CENTER = "health_center"
    SCHOOL = "school"
    DISPLACEMENT_SITE = "displacement_site"
    OTHER = "other"


class ItemCategory(StrEnum):
    FOOD = "food"
    WATER = "water"
    HEALTH = "health"
    HYGIENE = "hygiene"
    SHELTER = "shelter"
    EDUCATION = "education"
    OTHER = "other"


class InventoryTransactionType(StrEnum):
    INBOUND = "inbound"  # reception into the warehouse
    OUTBOUND = "outbound"  # dispatch (usually linked to a delivery)
    ADJUSTMENT = "adjustment"  # stock count correction (+/-)
    LOSS = "loss"  # damage, expiry, theft


class VehicleType(StrEnum):
    TRUCK = "truck"
    PICKUP = "pickup"
    VAN = "van"
    MOTORCYCLE = "motorcycle"


class VehicleStatus(StrEnum):
    AVAILABLE = "available"
    ON_MISSION = "on_mission"
    MAINTENANCE = "maintenance"
    OUT_OF_SERVICE = "out_of_service"


class DeliveryStatus(StrEnum):
    PLANNED = "planned"
    LOADING = "loading"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"
    DELAYED = "delayed"
    CANCELLED = "cancelled"


class DeliveryPriority(StrEnum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"


class RiskCategory(StrEnum):
    WEATHER = "weather"
    ROAD_CONDITION = "road_condition"
    SECURITY = "security"
    STOCK_SHORTAGE = "stock_shortage"
    VEHICLE = "vehicle"
    DELAY = "delay"
    OTHER = "other"


class AlertSeverity(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AlertStatus(StrEnum):
    OPEN = "open"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"
