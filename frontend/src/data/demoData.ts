/**
 * STATIC DEMONSTRATION DATA — entirely simulated.
 *
 * Used by the Overview page while the dashboard is not yet wired to the API.
 * It mirrors the backend seed (`backend/scripts/seed.py`) but does
 * NOT represent any real operation, organisation or person.
 */
import type { DeliverySummary, InventorySummary, Kpi, RiskAlertSummary } from '../types/domain'

export const DEMO_ORGANIZATION = {
  name: 'Alliance Humanitaire Teranga',
  shortName: 'AHT',
  country: 'Sénégal',
} as const

export const DEMO_USER = {
  name: 'Awa Ndiaye',
  role: 'Logistics Coordinator',
  initials: 'AN',
} as const

export const demoKpis: Kpi[] = [
  {
    id: 'total',
    label: 'Total Deliveries',
    value: 18,
    hint: 'Last 30 days',
    tone: 'neutral',
    trend: { label: '+4 vs. previous period', favorable: true },
  },
  {
    id: 'in-transit',
    label: 'In Transit',
    value: 5,
    hint: 'Currently on the road',
    tone: 'info',
    trend: { label: '3 arriving today', favorable: true },
  },
  {
    id: 'delivered',
    label: 'Delivered Successfully',
    value: 7,
    hint: '100 % proof of delivery',
    tone: 'success',
    trend: { label: '+2 vs. previous period', favorable: true },
  },
  {
    id: 'delayed',
    label: 'Delayed Deliveries',
    value: 3,
    hint: 'Above planned ETA',
    tone: 'warning',
    trend: { label: '+1 since yesterday', favorable: false },
  },
]

export const demoRecentDeliveries: DeliverySummary[] = [
  {
    reference: 'DLV-2026-0018',
    origin: 'Dakar — Hub central',
    destination: 'Koungheul',
    cargo: 'Kits alimentaires',
    status: 'in_transit',
    eta: '2026-11-13T16:30:00Z',
    vehicle: 'DK-5560-AC',
  },
  {
    reference: 'DLV-2026-0017',
    origin: 'Kaolack — Entrepôt régional',
    destination: 'Kaffrine',
    cargo: 'Moustiquaires',
    status: 'delayed',
    eta: '2026-11-13T11:00:00Z',
    vehicle: 'KL-2207-AC',
  },
  {
    reference: 'DLV-2026-0016',
    origin: 'Thiès — Entrepôt',
    destination: 'Mbour',
    cargo: 'Kits d’hygiène',
    status: 'delivered',
    eta: '2026-11-12T15:45:00Z',
    vehicle: 'TH-1190-AD',
  },
  {
    reference: 'DLV-2026-0015',
    origin: 'Tambacounda — Base Est',
    destination: 'Goudiry',
    cargo: 'Eau potable',
    status: 'loading',
    eta: '2026-11-14T09:00:00Z',
    vehicle: 'TC-7754-AA',
  },
  {
    reference: 'DLV-2026-0014',
    origin: 'Dakar — Hub central',
    destination: 'Diourbel',
    cargo: 'Médicaments essentiels',
    status: 'planned',
    eta: '2026-11-15T10:00:00Z',
    vehicle: 'Unassigned',
  },
]

export const demoRiskAlerts: RiskAlertSummary[] = [
  {
    id: 'ALR-031',
    title: 'Route dégradée sur la N1 entre Kaffrine et Koungheul',
    region: 'Kaffrine',
    severity: 'critical',
    status: 'open',
    raisedAt: '2026-11-13T07:20:00Z',
  },
  {
    id: 'ALR-030',
    title: 'Stock de moustiquaires sous le seuil de sécurité',
    region: 'Kaolack',
    severity: 'high',
    status: 'acknowledged',
    raisedAt: '2026-11-12T18:05:00Z',
  },
  {
    id: 'ALR-029',
    title: 'Retard de livraison supérieur à 3 h',
    region: 'Diourbel',
    severity: 'medium',
    status: 'open',
    raisedAt: '2026-11-12T14:40:00Z',
  },
  {
    id: 'ALR-028',
    title: 'Maintenance préventive requise — pick-up TC-8102-AD',
    region: 'Tambacounda',
    severity: 'low',
    status: 'open',
    raisedAt: '2026-11-11T09:15:00Z',
  },
]

export const demoInventory: InventorySummary[] = [
  { category: 'Kits alimentaires', warehouse: 'Dakar', quantity: 2400, unit: 'kits', coverageDays: 21, level: 'healthy' },
  { category: 'Eau potable', warehouse: 'Tambacounda', quantity: 18000, unit: 'litres', coverageDays: 12, level: 'healthy' },
  { category: 'Médicaments essentiels', warehouse: 'Dakar', quantity: 640, unit: 'boîtes', coverageDays: 9, level: 'low' },
  { category: 'Moustiquaires', warehouse: 'Kaolack', quantity: 180, unit: 'unités', coverageDays: 3, level: 'critical' },
]
