"""SIMULATED demonstration dataset for TerangaFlow.

Everything here is fictional: the organisation, people, vehicles, plates,
stock levels and events are invented for demonstration purposes and do NOT
describe real operations. Only the localities and their coordinates are real
(approximate town-centre coordinates, WGS 84).

Times are expressed as hour offsets from the seed "anchor" (today 08:00 UTC),
so the dataset always looks current whenever it is (re)loaded.
"""

from dataclasses import dataclass, field

from app.models.enums import (
    AlertSeverity,
    AlertStatus,
    DeliveryPriority,
    DeliveryStatus,
    DistributionPointType,
    ItemCategory,
    RiskCategory,
    VehicleStatus,
    VehicleType,
)

ORGANIZATION = {
    "slug": "alliance-humanitaire-teranga",
    "name": "Alliance Humanitaire Teranga (fictive)",
    "country_code": "SN",
    "contact_email": "contact@example.org",
}

# code, name, region, city, address, latitude, longitude, capacity_m3
WAREHOUSES = [
    ("WH-DKR", "Dakar — Hub central", "Dakar", "Dakar", "Zone industrielle de Hann (simulé)", 14.6928, -17.4467, 2400),
    ("WH-THS", "Thiès — Entrepôt", "Thiès", "Thiès", "Route de Mbour (simulé)", 14.7910, -16.9359, 900),
    ("WH-KLK", "Kaolack — Entrepôt régional", "Kaolack", "Kaolack", "Quartier Médina Baye (simulé)", 14.1500, -16.0726, 1200),
    ("WH-TBA", "Tambacounda — Base Est", "Tambacounda", "Tambacounda", "Route nationale 1 (simulé)", 13.7707, -13.6673, 1000),
]

# code, name, type, region, city, latitude, longitude, beneficiaries
DISTRIBUTION_POINTS = [
    ("DP-RUF", "Rufisque — Centre communautaire", DistributionPointType.COMMUNITY_CENTER, "Dakar", "Rufisque", 14.7167, -17.2667, 1800),
    ("DP-MBR", "Mbour — École élémentaire", DistributionPointType.SCHOOL, "Thiès", "Mbour", 14.4167, -16.9667, 950),
    ("DP-TIV", "Tivaouane — Poste de santé", DistributionPointType.HEALTH_CENTER, "Thiès", "Tivaouane", 14.9500, -16.8167, 1200),
    ("DP-DBL", "Diourbel — Centre de santé", DistributionPointType.HEALTH_CENTER, "Diourbel", "Diourbel", 14.6550, -16.2314, 2100),
    ("DP-NRO", "Nioro du Rip — Centre communautaire", DistributionPointType.COMMUNITY_CENTER, "Kaolack", "Nioro du Rip", 13.7500, -15.8000, 1400),
    ("DP-KAF", "Kaffrine — Centre communautaire", DistributionPointType.COMMUNITY_CENTER, "Kaffrine", "Kaffrine", 14.1059, -15.5508, 2600),
    ("DP-KGH", "Koungheul — Poste de santé", DistributionPointType.HEALTH_CENTER, "Kaffrine", "Koungheul", 13.9833, -14.8000, 1700),
    ("DP-GDY", "Goudiry — Site d'accueil", DistributionPointType.DISPLACEMENT_SITE, "Tambacounda", "Goudiry", 14.1833, -12.7167, 900),
    ("DP-BKL", "Bakel — Centre communautaire", DistributionPointType.COMMUNITY_CENTER, "Tambacounda", "Bakel", 14.9000, -12.4500, 1300),
]

# registration, label, type, status, capacity_kg, home warehouse, driver (fictional)
VEHICLES = [
    ("DK-4821-AB", "Camion 01", VehicleType.TRUCK, VehicleStatus.ON_MISSION, 12000, "WH-DKR", "Moussa Diop"),
    ("DK-3315-AF", "Pick-up 02", VehicleType.PICKUP, VehicleStatus.ON_MISSION, 1200, "WH-DKR", "Ibrahima Fall"),
    ("DK-5560-AC", "Camion 03", VehicleType.TRUCK, VehicleStatus.ON_MISSION, 10000, "WH-DKR", "Cheikh Sarr"),
    ("TH-1190-AD", "Fourgon 04", VehicleType.VAN, VehicleStatus.AVAILABLE, 2500, "WH-THS", "Mamadou Ba"),
    ("TH-2044-AA", "Pick-up 05", VehicleType.PICKUP, VehicleStatus.ON_MISSION, 1200, "WH-THS", "Ousmane Faye"),
    ("KL-2207-AC", "Camion 06", VehicleType.TRUCK, VehicleStatus.ON_MISSION, 10000, "WH-KLK", "Abdoulaye Ndiaye"),
    ("KL-6631-AB", "Fourgon 07", VehicleType.VAN, VehicleStatus.ON_MISSION, 2500, "WH-KLK", "Aliou Cissé"),
    ("TC-7754-AA", "Camion 08", VehicleType.TRUCK, VehicleStatus.ON_MISSION, 12000, "WH-TBA", "Samba Diallo"),
    ("TC-8102-AD", "Pick-up 09", VehicleType.PICKUP, VehicleStatus.MAINTENANCE, 1200, "WH-TBA", None),
    ("KF-0412-AB", "Moto 10", VehicleType.MOTORCYCLE, VehicleStatus.ON_MISSION, 150, "WH-KLK", "Pape Sow"),
]

# sku, name, category, unit, reorder level
CATALOG = {
    "FOOD-KIT": ("Kit alimentaire familial (riz, huile, lentilles)", ItemCategory.FOOD, "kits", 800),
    "WATER-L": ("Eau potable", ItemCategory.WATER, "litres", 6000),
    "MED-ESS": ("Médicaments essentiels", ItemCategory.HEALTH, "boîtes", 700),
    "NET-LLIN": ("Moustiquaire imprégnée (MILDA)", ItemCategory.HEALTH, "unités", 500),
    "HYG-KIT": ("Kit d'hygiène", ItemCategory.HYGIENE, "kits", 300),
    "TARP": ("Bâche abri", ItemCategory.SHELTER, "unités", 100),
    "EDU-KIT": ("Kit scolaire", ItemCategory.EDUCATION, "kits", 150),
}

# (warehouse, sku) -> current quantity after all seeded movements
STOCK = {
    ("WH-DKR", "FOOD-KIT"): 2400,
    ("WH-DKR", "MED-ESS"): 640,
    ("WH-DKR", "HYG-KIT"): 1100,
    ("WH-DKR", "TARP"): 420,
    ("WH-THS", "FOOD-KIT"): 900,
    ("WH-THS", "HYG-KIT"): 260,
    ("WH-THS", "EDU-KIT"): 380,
    ("WH-KLK", "FOOD-KIT"): 1300,
    ("WH-KLK", "NET-LLIN"): 180,
    ("WH-KLK", "WATER-L"): 9000,
    ("WH-TBA", "WATER-L"): 18000,
    ("WH-TBA", "FOOD-KIT"): 750,
    ("WH-TBA", "MED-ESS"): 210,
}


@dataclass(frozen=True)
class DeliverySeed:
    reference: str
    origin: str
    destination: str
    vehicle: str | None
    status: DeliveryStatus
    priority: DeliveryPriority
    cargo: str
    weight_kg: int
    planned_departure_h: int
    planned_arrival_h: int
    actual_departure_h: int | None = None
    actual_arrival_h: int | None = None
    notes: str | None = None
    # (sku, quantity) taken from the origin warehouse once the truck has left
    items: tuple[tuple[str, int], ...] = field(default_factory=tuple)


_S = DeliveryStatus
_P = DeliveryPriority

# 18 deliveries: 7 delivered, 5 in transit, 3 delayed, 1 loading, 1 planned, 1 cancelled.
# No vehicle is assigned to two active (loading / in transit / delayed) deliveries.
DELIVERIES = [
    DeliverySeed("DLV-2026-0001", "WH-DKR", "DP-RUF", "DK-3315-AF", _S.DELIVERED, _P.NORMAL, "Kits d'hygiène", 900, -400, -398, -400, -398, items=(("HYG-KIT", 150),)),
    DeliverySeed("DLV-2026-0002", "WH-THS", "DP-TIV", "TH-1190-AD", _S.DELIVERED, _P.HIGH, "Kits alimentaires", 2100, -340, -339, -340, -339, items=(("FOOD-KIT", 120),)),
    DeliverySeed("DLV-2026-0003", "WH-KLK", "DP-NRO", "KL-6631-AB", _S.DELIVERED, _P.NORMAL, "Moustiquaires", 600, -300, -298, -299, -297, items=(("NET-LLIN", 400),)),
    DeliverySeed("DLV-2026-0004", "WH-TBA", "DP-BKL", "TC-7754-AA", _S.DELIVERED, _P.URGENT, "Eau potable", 6000, -260, -254, -260, -253, items=(("WATER-L", 6000),)),
    DeliverySeed("DLV-2026-0005", "WH-DKR", "DP-DBL", "DK-4821-AB", _S.DELIVERED, _P.HIGH, "Médicaments essentiels", 1500, -200, -197, -200, -196, items=(("MED-ESS", 220),)),
    DeliverySeed("DLV-2026-0006", "WH-TBA", "DP-BKL", "TC-8102-AD", _S.DELAYED, _P.NORMAL, "Médicaments essentiels", 400, -10, -4, notes="Départ reporté : véhicule en maintenance (simulé)."),
    DeliverySeed("DLV-2026-0007", "WH-THS", "DP-MBR", "TH-2044-AA", _S.CANCELLED, _P.LOW, "Kits scolaires", 700, -120, -119, notes="Annulée : école fermée pendant la période d'examens (simulé)."),
    DeliverySeed("DLV-2026-0008", "WH-DKR", "DP-RUF", "DK-3315-AF", _S.IN_TRANSIT, _P.HIGH, "Bâches abri", 900, -1, 1, -1, items=(("TARP", 80),)),
    DeliverySeed("DLV-2026-0009", "WH-TBA", "DP-GDY", "TC-7754-AA", _S.DELIVERED, _P.URGENT, "Kits alimentaires", 3600, -60, -57, -60, -56, items=(("FOOD-KIT", 250),)),
    DeliverySeed("DLV-2026-0010", "WH-DKR", "DP-NRO", "DK-4821-AB", _S.IN_TRANSIT, _P.NORMAL, "Kits d'hygiène", 2400, -4, 3, -4, items=(("HYG-KIT", 300),)),
    DeliverySeed("DLV-2026-0011", "WH-KLK", "DP-NRO", "KL-6631-AB", _S.IN_TRANSIT, _P.HIGH, "Eau potable", 2000, -2, 1, -2, items=(("WATER-L", 2000),)),
    DeliverySeed("DLV-2026-0012", "WH-THS", "DP-DBL", "TH-2044-AA", _S.DELAYED, _P.HIGH, "Kits alimentaires", 900, -6, -3, -5, notes="Panne mineure signalée à Bambey (simulé).", items=(("FOOD-KIT", 60),)),
    DeliverySeed("DLV-2026-0013", "WH-KLK", "DP-KAF", "KF-0412-AB", _S.IN_TRANSIT, _P.URGENT, "Médicaments (petit colis)", 40, -1, 1, -1),
    DeliverySeed("DLV-2026-0014", "WH-DKR", "DP-DBL", None, _S.PLANNED, _P.NORMAL, "Médicaments essentiels", 1200, 50, 53),
    DeliverySeed("DLV-2026-0015", "WH-TBA", "DP-GDY", "TC-7754-AA", _S.LOADING, _P.HIGH, "Eau potable", 1000, 25, 28),
    DeliverySeed("DLV-2026-0016", "WH-THS", "DP-MBR", "TH-1190-AD", _S.DELIVERED, _P.NORMAL, "Kits d'hygiène", 800, -30, -28, -30, -27, items=(("HYG-KIT", 120),)),
    DeliverySeed("DLV-2026-0017", "WH-KLK", "DP-KAF", "KL-2207-AC", _S.DELAYED, _P.HIGH, "Moustiquaires", 700, -8, -5, -7, notes="Route dégradée sur la N1 (simulé).", items=(("NET-LLIN", 350),)),
    DeliverySeed("DLV-2026-0018", "WH-DKR", "DP-KGH", "DK-5560-AC", _S.IN_TRANSIT, _P.URGENT, "Kits alimentaires", 6000, -6, 8, -6, items=(("FOOD-KIT", 400),)),
]


@dataclass(frozen=True)
class AlertSeed:
    reference: str
    title: str
    description: str
    category: RiskCategory
    severity: AlertSeverity
    status: AlertStatus
    region: str
    detected_h: int
    resolved_h: int | None = None
    delivery: str | None = None
    warehouse: str | None = None
    distribution_point: str | None = None
    vehicle: str | None = None


ALERTS = [
    AlertSeed("ALR-026", "Fortes pluies annoncées sur l'axe Tambacounda–Bakel", "Scénario simulé : risque de routes impraticables pendant 48 h.", RiskCategory.WEATHER, AlertSeverity.MEDIUM, AlertStatus.RESOLVED, "Tambacounda", -270, resolved_h=-240, distribution_point="DP-BKL"),
    AlertSeed("ALR-027", "Retard au chargement — entrepôt de Thiès", "Scénario simulé : file d'attente au quai de chargement.", RiskCategory.DELAY, AlertSeverity.LOW, AlertStatus.RESOLVED, "Thiès", -122, resolved_h=-118, warehouse="WH-THS"),
    AlertSeed("ALR-028", "Maintenance préventive requise — pick-up TC-8102-AD", "Scénario simulé : vidange et freins hors tolérance.", RiskCategory.VEHICLE, AlertSeverity.LOW, AlertStatus.OPEN, "Tambacounda", -47, vehicle="TC-8102-AD"),
    AlertSeed("ALR-029", "Retard de livraison supérieur à 3 h", "Scénario simulé : DLV-2026-0012 n'est pas arrivée à Diourbel.", RiskCategory.DELAY, AlertSeverity.MEDIUM, AlertStatus.OPEN, "Diourbel", -2, delivery="DLV-2026-0012"),
    AlertSeed("ALR-030", "Stock de moustiquaires sous le seuil de sécurité", "Scénario simulé : 180 unités restantes pour un seuil de 500.", RiskCategory.STOCK_SHORTAGE, AlertSeverity.HIGH, AlertStatus.ACKNOWLEDGED, "Kaolack", -14, warehouse="WH-KLK"),
    AlertSeed("ALR-031", "Route dégradée sur la N1 entre Kaffrine et Koungheul", "Scénario simulé : chaussée endommagée, vitesse fortement réduite.", RiskCategory.ROAD_CONDITION, AlertSeverity.CRITICAL, AlertStatus.OPEN, "Kaffrine", -1, delivery="DLV-2026-0017"),
]
