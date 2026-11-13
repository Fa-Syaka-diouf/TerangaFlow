import { Link } from 'react-router'
import type { DeliverySummary } from '../../types/domain'
import { formatDateTime } from '../../utils/format'
import { DeliveryStatusBadge } from '../ui/Badge'
import { Card, CardHeader } from '../ui/Card'
import { Icon } from '../ui/Icon'

export function RecentDeliveries({ deliveries }: { deliveries: DeliverySummary[] }) {
  return (
    <Card className="overflow-hidden">
      <CardHeader
        title="Recent Deliveries"
        description="Latest dispatches across the network"
        action={
          <Link
            to="/deliveries"
            className="inline-flex items-center gap-1 text-sm font-medium text-brand-800 hover:text-brand-600"
          >
            View all <Icon name="arrowRight" size={14} />
          </Link>
        }
      />

      {/* Table on md+ */}
      <div className="hidden overflow-x-auto md:block">
        <table className="w-full text-left text-sm">
          <thead>
            <tr className="border-b border-line text-xs text-muted">
              <th className="px-5 py-2.5 font-medium">Reference</th>
              <th className="px-3 py-2.5 font-medium">Route</th>
              <th className="px-3 py-2.5 font-medium">Cargo</th>
              <th className="px-3 py-2.5 font-medium">ETA</th>
              <th className="px-5 py-2.5 text-right font-medium">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-line">
            {deliveries.map((delivery) => (
              <tr key={delivery.reference} className="hover:bg-slate-50/70">
                <td className="px-5 py-3.5">
                  <p className="font-medium whitespace-nowrap text-ink tabular-nums">{delivery.reference}</p>
                  <p className="text-xs text-muted">{delivery.vehicle}</p>
                </td>
                <td className="px-3 py-3.5">
                  <p className="text-ink">{delivery.destination}</p>
                  <p className="text-xs text-muted">from {delivery.origin}</p>
                </td>
                <td className="px-3 py-3.5 text-slate-600">{delivery.cargo}</td>
                <td className="px-3 py-3.5 whitespace-nowrap text-slate-600 tabular-nums">
                  {formatDateTime(delivery.eta)}
                </td>
                <td className="px-5 py-3.5 text-right">
                  <DeliveryStatusBadge status={delivery.status} />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Stacked list on mobile */}
      <ul className="divide-y divide-line md:hidden">
        {deliveries.map((delivery) => (
          <li key={delivery.reference} className="flex items-start justify-between gap-3 px-5 py-3.5">
            <div className="min-w-0">
              <p className="text-sm font-medium text-ink">{delivery.destination}</p>
              <p className="truncate text-xs text-muted">
                {delivery.reference} · {delivery.cargo}
              </p>
              <p className="mt-0.5 text-xs text-muted">ETA {formatDateTime(delivery.eta)}</p>
            </div>
            <DeliveryStatusBadge status={delivery.status} />
          </li>
        ))}
      </ul>
    </Card>
  )
}
