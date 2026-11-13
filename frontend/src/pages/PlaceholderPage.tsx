import { Link } from 'react-router'
import { PageHeader } from '../components/layout/PageHeader'
import type { NavItem } from '../components/layout/navigation'
import { Icon } from '../components/ui/Icon'

/** Clean placeholder for modules scheduled in later phases. */
export function PlaceholderPage({ item }: { item: NavItem }) {
  return (
    <>
      <PageHeader title={item.label} description={item.description} />
      <div className="grid place-items-center rounded-2xl border border-dashed border-slate-300 bg-white px-6 py-20 text-center">
        <span className="grid size-12 place-items-center rounded-xl bg-brand-50 text-brand-800 ring-1 ring-brand-100">
          <Icon name={item.icon} size={22} />
        </span>
        <h2 className="mt-4 font-display text-lg font-bold text-ink">{item.label} is on the roadmap</h2>
        <p className="mt-1.5 max-w-md text-sm text-muted">
          This module will be delivered in an upcoming phase. The navigation, layout and API foundations are already
          in place.
        </p>
        <Link
          to="/"
          className="mt-6 inline-flex items-center gap-1.5 rounded-lg bg-brand-900 px-4 py-2 text-sm font-medium text-white hover:bg-brand-800"
        >
          Back to Overview <Icon name="arrowRight" size={15} />
        </Link>
      </div>
    </>
  )
}
