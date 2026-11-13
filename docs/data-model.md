# Modèle de données — phase 1

Schéma PostgreSQL initial de TerangaFlow (migration Alembic `a79f481c6812_initial_schema`).
Source de vérité : `backend/app/models/`.

## Principes

- **Multi-organisation** : chaque table métier porte `organization_id` (FK → `organizations.id`, `ON DELETE CASCADE`, `NOT NULL`).
  Chaque table a une contrainte unique ou un index composite qui commence par `organization_id` : PostgreSQL l'utilise pour filtrer par organisation.
- **Clés primaires** : `UUID`, générées côté application (`uuid4`) et côté base (`gen_random_uuid()`).
- **Clés naturelles** uniques par organisation (`code`, `reference`, `registration_number`) : elles servent au seed idempotent et aux intégrations futures.
- **Statuts** : types `ENUM` PostgreSQL natifs, en minuscules. Ils sont dupliqués côté frontend dans `frontend/src/types/domain.ts`.
- **Horodatage** : `created_at` et `updated_at` en `timestamptz`, avec `DEFAULT now()`. L'ORM met à jour `updated_at` (`onupdate`). `inventory_transactions` est un registre immuable : seulement `created_at`.
- **Quantités** en `NUMERIC(14,3)`, **coordonnées** en `NUMERIC(9,6)` (WGS 84), avec des contraintes de plage.
- **Nommage** déterministe des contraintes (`pk_`, `fk_`, `uq_`, `ck_`, `ix_`) pour des migrations stables.

## Tables

| Table | Rôle | Clé naturelle | Relations principales |
|---|---|---|---|
| `organizations` | ONG (tenant) | `slug` | — |
| `warehouses` | Entrepôts | `(organization_id, code)` | — |
| `distribution_points` | Points de distribution (bénéficiaires) | `(organization_id, code)` | — |
| `inventory_items` | Stock courant d'un article (SKU) dans un entrepôt | `(warehouse_id, sku)` | → `warehouses` (CASCADE) |
| `inventory_transactions` | Mouvements de stock signés (+ entrée / − sortie) | `(organization_id, reference)` | → `inventory_items` (CASCADE), → `deliveries` (SET NULL) |
| `vehicles` | Flotte | `(organization_id, registration_number)` | → `warehouses` (base, SET NULL) |
| `deliveries` | Livraison entrepôt → point de distribution | `(organization_id, reference)` | → `warehouses`, `distribution_points` (RESTRICT), → `vehicles` (SET NULL) |
| `risk_alerts` | Alertes de risque | `(organization_id, reference)` | → `deliveries`, `warehouses`, `distribution_points`, `vehicles` (SET NULL) |

## ENUMs

| Type | Valeurs |
|---|---|
| `distribution_point_type` | community_center, health_center, school, displacement_site, other |
| `item_category` | food, water, health, hygiene, shelter, education, other |
| `inventory_transaction_type` | inbound, outbound, adjustment, loss |
| `vehicle_type` | truck, pickup, van, motorcycle |
| `vehicle_status` | available, on_mission, maintenance, out_of_service |
| `delivery_status` | planned, loading, in_transit, delivered, delayed, cancelled |
| `delivery_priority` | low, normal, high, urgent |
| `risk_category` | weather, road_condition, security, stock_shortage, vehicle, delay, other |
| `alert_severity` | low, medium, high, critical |
| `alert_status` | open, acknowledged, resolved |

## Contraintes métier notables

- `inventory_items.quantity >= 0` ; `inventory_transactions.quantity_change <> 0`, avec un signe cohérent avec le type de mouvement (`inbound` > 0, `outbound`/`loss` < 0, `adjustment` libre).
- `deliveries` : `planned_arrival_at >= planned_departure_at` ; arrivée réelle ≥ départ réel ; un statut `delivered` exige `actual_arrival_at`.
- `risk_alerts` : `resolved_at` est renseigné **si et seulement si** `status = 'resolved'`.

## Limites assumées (évolutions possibles)

- La base ne garantit pas encore que deux lignes liées appartiennent à la même organisation, par exemple une livraison et son entrepôt (il faudrait des FK composites). Ce contrôle relèvera de la couche service.
- `updated_at` est mis à jour par l'ORM, pas par un trigger : les écritures SQL directes ne le modifient pas.
- Une livraison ne détaille pas encore ses lignes d'articles. Les sorties de stock sont reliées à la livraison via `inventory_transactions.delivery_id`.
