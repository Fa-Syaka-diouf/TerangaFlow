import type { Kpi, KpiTone } from '../../types/domain'
import { cn, formatNumber } from '../../utils/format'
import { Icon, type IconName } from '../ui/Icon'

const toneStyles: Record<KpiTone, { icon: IconName; chip: string; accent: string }> = {
  neutral: { icon: 'truck', chip: 'bg-slate-100 text-slate-700', accent: 'bg-slate-300' },
  info: { icon: 'arrowRight', chip: 'bg-info-soft text-info', accent: 'bg-info' },
  success: { icon: 'check', chip: 'bg-brand-50 text-brand-800', accent: 'bg-brand-600' },
  warning: { icon: 'clock', chip: 'bg-alert-soft text-amber-700', accent: 'bg-alert' },
}

export function KpiCard({ kpi }: { kpi: Kpi }) {
  const style = toneStyles[kpi.tone]

  return (
    <article className="relative overflow-hidden rounded-2xl border border-line bg-white p-5 shadow-card">
      <span className={cn('absolute inset-x-0 top-0 h-0.75', style.accent)} aria-hidden="true" />
      <div className="flex items-start justify-between gap-3">
        <p className="text-[13px] font-medium text-muted">{kpi.label}</p>
        <span className={cn('grid size-8 place-items-center rounded-lg', style.chip)}>
          <Icon name={style.icon} size={16} strokeWidth={2} />
        </span>
      </div>
      <p className="mt-3 font-display text-[34px] leading-none font-extrabold tracking-tight text-ink tabular-nums">
        {formatNumber(kpi.value)}
      </p>
      <p className="mt-1.5 text-xs text-muted">{kpi.hint}</p>
      <p
        className={cn(
          'mt-4 inline-flex items-center gap-1 text-xs font-medium',
          kpi.trend.favorable ? 'text-brand-800' : 'text-critical',
        )}
      >
        <Icon name={kpi.trend.favorable ? 'arrowUpRight' : 'arrowDownRight'} size={14} strokeWidth={2} />
        {kpi.trend.label}
      </p>
    </article>
  )
}
