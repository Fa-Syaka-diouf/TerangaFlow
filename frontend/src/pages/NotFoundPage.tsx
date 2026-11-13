import { Link } from 'react-router'

export function NotFoundPage() {
  return (
    <div className="grid place-items-center py-24 text-center">
      <p className="font-display text-sm font-bold tracking-widest text-brand-600">404</p>
      <h1 className="mt-2 font-display text-2xl font-extrabold text-ink">Page not found</h1>
      <p className="mt-2 text-sm text-muted">The page you are looking for does not exist.</p>
      <Link to="/" className="mt-6 text-sm font-medium text-brand-800 hover:text-brand-600">
        Return to Overview →
      </Link>
    </div>
  )
}
