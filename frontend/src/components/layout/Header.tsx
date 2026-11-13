import { DEMO_ORGANIZATION, DEMO_USER } from '../../data/demoData'
import { useApiHealth, type ApiHealthState } from '../../hooks/useApiHealth'
import { cn } from '../../utils/format'
import { Icon } from '../ui/Icon'

const apiStatusMeta: Record<ApiHealthState, { label: string; dot: string }> = {
  checking: { label: 'Checking API…', dot: 'bg-slate-300' },
  online: { label: 'API online', dot: 'bg-brand-600' },
  offline: { label: 'API offline', dot: 'bg-critical' },
}

interface HeaderProps {
  onOpenNavigation: () => void
}

export function Header({ onOpenNavigation }: HeaderProps) {
  const apiState = useApiHealth()
  const apiStatus = apiStatusMeta[apiState]

  return (
    <header className="sticky top-0 z-20 flex h-16 items-center gap-3 border-b border-line bg-white/85 px-4 backdrop-blur-md sm:px-6 lg:px-8">
      <button
        type="button"
        onClick={onOpenNavigation}
        className="-ml-1 rounded-lg p-2 text-muted hover:bg-slate-100 hover:text-ink lg:hidden"
        aria-label="Open navigation"
      >
        <Icon name="menu" />
      </button>

      {/* Organisation switcher (static for now) */}
      <button
        type="button"
        className="flex min-w-0 items-center gap-2.5 rounded-lg py-1.5 pr-2 pl-1.5 text-left hover:bg-slate-50"
      >
        <span className="grid size-8 shrink-0 place-items-center rounded-lg bg-sand font-display text-xs font-extrabold text-ochre">
          {DEMO_ORGANIZATION.shortName}
        </span>
        <span className="min-w-0">
          <span className="block truncate text-sm font-semibold text-ink">{DEMO_ORGANIZATION.name}</span>
          <span className="block text-xs text-muted">Fictional organisation · {DEMO_ORGANIZATION.country}</span>
        </span>
        <Icon name="chevronDown" size={16} className="hidden shrink-0 text-muted sm:block" />
      </button>

      <div className="ml-auto flex items-center gap-2 sm:gap-3">
        <label className="relative hidden md:block">
          <span className="sr-only">Search</span>
          <Icon name="search" size={16} className="pointer-events-none absolute top-1/2 left-3 -translate-y-1/2 text-muted" />
          <input
            type="search"
            placeholder="Search deliveries, sites…"
            className="h-9 w-60 rounded-lg border border-line bg-surface pr-3 pl-9 text-sm placeholder:text-slate-400 focus:border-brand-600 focus:bg-white focus:outline-none xl:w-72"
          />
        </label>

        <span
          className="hidden items-center gap-2 rounded-full border border-line px-2.5 py-1 text-xs font-medium text-muted sm:inline-flex"
          title="Live status of GET /api/v1/health"
        >
          <span className={cn('size-2 rounded-full', apiStatus.dot, apiState === 'checking' && 'animate-pulse')} />
          {apiStatus.label}
        </span>

        <button
          type="button"
          className="relative rounded-lg p-2 text-muted hover:bg-slate-100 hover:text-ink"
          aria-label="Notifications"
        >
          <Icon name="bell" />
          <span className="absolute top-1.5 right-1.5 size-2 rounded-full bg-alert ring-2 ring-white" />
        </button>

        <div className="flex items-center gap-2.5 border-l border-line pl-3">
          <span className="grid size-9 place-items-center rounded-full bg-brand-900 text-xs font-semibold text-white">
            {DEMO_USER.initials}
          </span>
          <span className="hidden leading-tight xl:block">
            <span className="block text-sm font-semibold text-ink">{DEMO_USER.name}</span>
            <span className="block text-xs text-muted">{DEMO_USER.role}</span>
          </span>
        </div>
      </div>
    </header>
  )
}
