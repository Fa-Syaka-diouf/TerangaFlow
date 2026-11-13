/**
 * Domain types shared by the UI. Status unions mirror the PostgreSQL
 * ENUMs defined in the backend (`backend/app/models/enums.py`).
 */
export type DeliveryStatus =
  | 'planned'
  | 'loading'
  | 'in_transit'
  | 'delivered'
  | 'delayed'
  | 'cancelled'

export type AlertSeverity = 'low' | 'medium' | 'high' | 'critical'

export type AlertStatus = 'open' | 'acknowledged' | 'resolved'

export type StockLevel = 'healthy' | 'low' | 'critical'

export type KpiTone = 'neutral' | 'info' | 'success' | 'warning'

export interface Kpi {
  id: string
  label: string
  value: number
  hint: string
  tone: KpiTone
  trend: { label: string; favorable: boolean }
}

export interface DeliverySummary {
  reference: string
  origin: string
  destination: string
  cargo: string
  status: DeliveryStatus
  eta: string
  vehicle: string
}

export interface RiskAlertSummary {
  id: string
  title: string
  region: string
  severity: AlertSeverity
  status: AlertStatus
  raisedAt: string
}

export interface InventorySummary {
  category: string
  warehouse: string
  quantity: number
  unit: string
  coverageDays: number
  level: StockLevel
}
