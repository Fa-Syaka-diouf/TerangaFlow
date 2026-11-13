import { NavLink } from 'react-router'
import { cn } from '../../utils/format'
import { Icon } from '../ui/Icon'
import { Logo } from './Logo'
import { navSections } from './navigation'

interface SidebarProps {
  open: boolean
  onClose: () => void
}

/**
 * Discreet geometric band inspired by West-African woven textiles —
 * kept at very low opacity so it reads as texture, not decoration.
 */
function WovenBand() {
  return (
    <svg className="h-3 w-full text-white/10" aria-hidden="true">
      <defs>
        <pattern id="tf-weave" width="16" height="12" patternUnits="userSpaceOnUse">
          <path d="M0 12 8 4l8 8" fill="none" stroke="currentColor" strokeWidth="1.2" />
          <path d="M4 12 8 8l4 4" fill="currentColor" />
        </pattern>
      </defs>
      <rect width="100%" height="12" fill="url(#tf-weave)" />
    </svg>
  )
}

export function Sidebar({ open, onClose }: SidebarProps) {
  return (
    <>
      {/* Mobile backdrop */}
      <div
        className={cn(
          'fixed inset-0 z-30 bg-ink/40 backdrop-blur-[2px] transition-opacity lg:hidden',
          open ? 'opacity-100' : 'pointer-events-none opacity-0',
        )}
        onClick={onClose}
        aria-hidden="true"
      />

      <aside
        className={cn(
          'fixed inset-y-0 left-0 z-40 flex w-68 flex-col bg-brand-900 text-white transition-transform duration-200 lg:translate-x-0',
          open ? 'translate-x-0' : '-translate-x-full',
        )}
        aria-label="Main navigation"
      >
        <div className="flex h-16 items-center justify-between px-5">
          <Logo />
          <button
            type="button"
            onClick={onClose}
            className="rounded-lg p-1.5 text-white/70 hover:bg-white/10 hover:text-white lg:hidden"
            aria-label="Close navigation"
          >
            <Icon name="close" />
          </button>
        </div>

        <nav className="flex-1 overflow-y-auto px-3 pt-4 pb-6">
          {navSections.map((section) => (
            <div key={section.title} className="mb-6">
              <p className="px-3 pb-2 text-[11px] font-semibold uppercase tracking-[0.12em] text-white/40">
                {section.title}
              </p>
              <ul className="space-y-0.5">
                {section.items.map((item) => (
                  <li key={item.path}>
                    <NavLink
                      to={item.path}
                      end={item.path === '/'}
                      onClick={onClose}
                      className={({ isActive }) =>
                        cn(
                          'group relative flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors',
                          isActive
                            ? 'bg-white/10 text-white'
                            : 'text-white/65 hover:bg-white/5 hover:text-white',
                        )
                      }
                    >
                      {({ isActive }) => (
                        <>
                          <span
                            className={cn(
                              'absolute top-1/2 left-0 h-5 w-0.75 -translate-y-1/2 rounded-r-full bg-brand-400 transition-opacity',
                              isActive ? 'opacity-100' : 'opacity-0',
                            )}
                            aria-hidden="true"
                          />
                          <Icon
                            name={item.icon}
                            size={18}
                            className={isActive ? 'text-brand-400' : 'text-white/50 group-hover:text-white/80'}
                          />
                          {item.label}
                        </>
                      )}
                    </NavLink>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </nav>

        <div className="px-5 pb-5">
          <WovenBand />
          <div className="mt-4 rounded-xl bg-white/5 p-3.5 ring-1 ring-white/10">
            <p className="text-xs font-semibold text-white">Phase 1 · Foundations</p>
            <p className="mt-1 text-xs leading-relaxed text-white/55">
              Dashboard figures are simulated demonstration data.
            </p>
          </div>
        </div>
      </aside>
    </>
  )
}
