import type { ReactNode } from 'react'
import type { AlertSeverity, DeliveryStatus, StockLevel } from '../../types/domain'
import { cn } from '../../utils/format'

export type BadgeTone = 'neutral' | 'brand' | 'info' | 'warning' | 'critical' | 'muted'

const toneClasses: Record<BadgeTone, { badge: string; dot: string }> = {
  neutral: { badge: 'bg-slate-100 text-slate-700', dot: 'bg-slate-400' },
  brand: { badge: 'bg-brand-50 text-brand-800 ring-1 ring-brand-100', dot: 'bg-brand-600' },
  info: { badge: 'bg-info-soft text-info', dot: 'bg-info' },
  warning: { badge: 'bg-alert-soft text-amber-800', dot: 'bg-alert' },
  critical: { badge: 'bg-critical-soft text-red-800', dot: 'bg-critical' },
  muted: { badge: 'bg-slate-50 text-slate-500 ring-1 ring-line', dot: 'bg-slate-300' },
}

interface BadgeProps {
  tone?: BadgeTone
  children: ReactNode
  dot?: boolean
  className?: string
}

export function Badge({ tone = 'neutral', children, dot = true, className }: BadgeProps) {
  const classes = toneClasses[tone]
  return (
    <span
      className={cn(
        'inline-flex items-center gap-1.5 whitespace-nowrap rounded-full px-2.5 py-0.5 text-xs font-medium',
        classes.badge,
        className,
      )}
    >
      {dot && <span className={cn('size-1.5 rounded-full', classes.dot)} aria-hidden="true" />}
      {children}
    </span>
  )
}

const deliveryStatusMeta: Record<DeliveryStatus, { label: string; tone: BadgeTone }> = {
  planned: { label: 'Planned', tone: 'muted' },
  loading: { label: 'Loading', tone: 'neutral' },
  in_transit: { label: 'In transit', tone: 'info' },
  delivered: { label: 'Delivered', tone: 'brand' },
  delayed: { label: 'Delayed', tone: 'warning' },
  cancelled: { label: 'Cancelled', tone: 'critical' },
}

export function DeliveryStatusBadge({ status }: { status: DeliveryStatus }) {
  const meta = deliveryStatusMeta[status]
  return <Badge tone={meta.tone}>{meta.label}</Badge>
}

const severityMeta: Record<AlertSeverity, { label: string; tone: BadgeTone }> = {
  low: { label: 'Low', tone: 'muted' },
  medium: { label: 'Medium', tone: 'neutral' },
  high: { label: 'High', tone: 'warning' },
  critical: { label: 'Critical', tone: 'critical' },
}

export function SeverityBadge({ severity }: { severity: AlertSeverity }) {
  const meta = severityMeta[severity]
  return <Badge tone={meta.tone}>{meta.label}</Badge>
}

const stockLevelMeta: Record<StockLevel, { label: string; tone: BadgeTone }> = {
  healthy: { label: 'Healthy', tone: 'brand' },
  low: { label: 'Low', tone: 'warning' },
  critical: { label: 'Critical', tone: 'critical' },
}

export function StockLevelBadge({ level }: { level: StockLevel }) {
  const meta = stockLevelMeta[level]
  return <Badge tone={meta.tone}>{meta.label}</Badge>
}

/** Explicit marker shown wherever simulated data is displayed. */
export function DemoDataBadge() {
  return (
    <span className="inline-flex items-center gap-1 rounded-md border border-dashed border-amber-300 bg-amber-50 px-2 py-0.5 text-[11px] font-semibold uppercase tracking-wide text-amber-800">
      Demo data
    </span>
  )
}
