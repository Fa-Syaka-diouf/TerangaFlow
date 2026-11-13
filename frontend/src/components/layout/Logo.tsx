/** TerangaFlow mark: a "T" whose stem turns into a route arrow. */
export function Logo() {
  return (
    <div className="flex items-center gap-2.5">
      <svg width="34" height="34" viewBox="0 0 32 32" fill="none" aria-hidden="true">
        <rect width="32" height="32" rx="9" fill="#F8FAFC" fillOpacity="0.08" />
        <rect x="0.5" y="0.5" width="31" height="31" rx="8.5" stroke="#F8FAFC" strokeOpacity="0.14" />
        <path d="M9 11h14M16 11v12" stroke="#F8FAFC" strokeWidth="2.6" strokeLinecap="round" />
        <path
          d="M19.5 19.5l3.5 3.5M23 19.5v3.5h-3.5"
          stroke="#4ADE80"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
      <div className="leading-none">
        <span className="font-display text-[17px] font-extrabold tracking-tight text-white">
          Teranga<span className="text-brand-400">Flow</span>
        </span>
        <span className="mt-1 block text-[10.5px] font-medium uppercase tracking-[0.14em] text-white/45">
          Logistics Control
        </span>
      </div>
    </div>
  )
}
