import { InventoryStatus } from '../components/dashboard/InventoryStatus'
import { KpiCard } from '../components/dashboard/KpiCard'
import { RecentDeliveries } from '../components/dashboard/RecentDeliveries'
import { RecentRiskAlerts } from '../components/dashboard/RecentRiskAlerts'
import { PageHeader } from '../components/layout/PageHeader'
import { DemoDataBadge } from '../components/ui/Badge'
import { Icon } from '../components/ui/Icon'
import {
  demoInventory,
  demoKpis,
  demoRecentDeliveries,
  demoRiskAlerts,
} from '../data/demoData'

export function OverviewPage() {
  return (
    <>
      <PageHeader
        title="Overview"
        description="Operational snapshot of deliveries, stock and risks across your Senegal network."
        meta={
          <>
            <DemoDataBadge />
            <span className="text-xs text-muted">Last 30 days · Dakar, Thiès, Kaolack, Kaffrine, Tambacounda</span>
          </>
        }
      />

      <div
        role="note"
        className="mb-6 flex items-start gap-3 rounded-xl border border-amber-200 bg-amber-50/70 px-4 py-3 text-sm text-amber-900"
      >
        <Icon name="info" size={18} className="mt-0.5 shrink-0 text-alert" />
        <p>
          All figures on this page are <strong className="font-semibold">simulated demonstration data</strong> for a
          fictional organisation. They do not describe real operations.
        </p>
      </div>

      <section aria-label="Key indicators" className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {demoKpis.map((kpi) => (
          <KpiCard key={kpi.id} kpi={kpi} />
        ))}
      </section>

      <div className="mt-6 grid gap-6 xl:grid-cols-3">
        <div className="xl:col-span-2">
          <RecentDeliveries deliveries={demoRecentDeliveries} />
        </div>
        <InventoryStatus items={demoInventory} />
      </div>

      <div className="mt-6">
        <RecentRiskAlerts alerts={demoRiskAlerts} />
      </div>
    </>
  )
}
