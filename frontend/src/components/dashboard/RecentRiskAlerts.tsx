import { Link } from 'react-router'
import type { AlertSeverity, AlertStatus, RiskAlertSummary } from '../../types/domain'
import { cn, formatDateTime } from '../../utils/format'
import { SeverityBadge } from '../ui/Badge'
import { Card, CardHeader } from '../ui/Card'
import { Icon } from '../ui/Icon'

const severityRail: Record<AlertSeverity, string> = {
  low: 'bg-slate-300',
  medium: 'bg-slate-500',
  high: 'bg-alert',
  critical: 'bg-critical',
}

const statusLabel: Record<AlertStatus, string> = {
  open: 'Open',
  acknowledged: 'Acknowledged',
  resolved: 'Resolved',
}

export function RecentRiskAlerts({ alerts }: { alerts: RiskAlertSummary[] }) {
  const openCount = alerts.filter((alert) => alert.status === 'open').length

  return (
    <Card>
      <CardHeader
        title="Recent Risk Alerts"
        description={`${openCount} open · requires attention`}
        action={
          <Link
            to="/risk-alerts"
            className="inline-flex items-center gap-1 text-sm font-medium text-brand-800 hover:text-brand-600"
          >
            View all <Icon name="arrowRight" size={14} />
          </Link>
        }
      />
      <ul className="divide-y divide-line">
        {alerts.map((alert) => (
          <li key={alert.id} className="flex gap-3.5 px-5 py-4">
            <span className={cn('w-1 shrink-0 rounded-full', severityRail[alert.severity])} aria-hidden="true" />
            <div className="min-w-0 flex-1">
              <div className="flex items-start justify-between gap-3">
                <p className="text-sm leading-snug font-medium text-ink">{alert.title}</p>
                <SeverityBadge severity={alert.severity} />
              </div>
              <p className="mt-1.5 flex flex-wrap items-center gap-x-3 gap-y-1 text-xs text-muted">
                <span className="inline-flex items-center gap-1">
                  <Icon name="pin" size={13} /> {alert.region}
                </span>
                <span className="tabular-nums">{formatDateTime(alert.raisedAt)}</span>
                <span>{statusLabel[alert.status]}</span>
              </p>
            </div>
          </li>
        ))}
      </ul>
    </Card>
  )
}
