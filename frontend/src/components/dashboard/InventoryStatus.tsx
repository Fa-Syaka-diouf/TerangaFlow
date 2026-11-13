import type { InventorySummary, StockLevel } from '../../types/domain'
import { cn, formatNumber } from '../../utils/format'
import { StockLevelBadge } from '../ui/Badge'
import { Card, CardHeader } from '../ui/Card'

/** Coverage bar is capped at 30 days of stock. */
const COVERAGE_TARGET_DAYS = 30

const barColor: Record<StockLevel, string> = {
  healthy: 'bg-brand-600',
  low: 'bg-alert',
  critical: 'bg-critical',
}

export function InventoryStatus({ items }: { items: InventorySummary[] }) {
  const atRisk = items.filter((item) => item.level !== 'healthy').length

  return (
    <Card>
      <CardHeader title="Inventory Status" description={`${atRisk} of ${items.length} key categories below target`} />
      <ul className="space-y-5 px-5 py-5">
        {items.map((item) => {
          const ratio = Math.min(item.coverageDays / COVERAGE_TARGET_DAYS, 1)
          return (
            <li key={`${item.category}-${item.warehouse}`}>
              <div className="flex items-start justify-between gap-3">
                <div className="min-w-0">
                  <p className="truncate text-sm font-medium text-ink">{item.category}</p>
                  <p className="text-xs text-muted">
                    {formatNumber(item.quantity)} {item.unit} · {item.warehouse}
                  </p>
                </div>
                <StockLevelBadge level={item.level} />
              </div>
              <div className="mt-2.5 flex items-center gap-3">
                <div
                  className="h-1.5 flex-1 overflow-hidden rounded-full bg-slate-100"
                  role="meter"
                  aria-valuemin={0}
                  aria-valuemax={COVERAGE_TARGET_DAYS}
                  aria-valuenow={item.coverageDays}
                  aria-label={`${item.category} stock coverage`}
                >
                  <div
                    className={cn('h-full rounded-full', barColor[item.level])}
                    style={{ width: `${ratio * 100}%` }}
                  />
                </div>
                <span className="w-14 text-right text-xs font-medium text-slate-600 tabular-nums">
                  {item.coverageDays} days
                </span>
              </div>
            </li>
          )
        })}
      </ul>
    </Card>
  )
}
