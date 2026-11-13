import type { IconName } from '../ui/Icon'

export interface NavItem {
  label: string
  path: string
  icon: IconName
  description: string
}

export interface NavSection {
  title: string
  items: NavItem[]
}

/** Single source of truth for the sidebar, the header title and the routes. */
export const navSections: NavSection[] = [
  {
    title: 'Operations',
    items: [
      { label: 'Overview', path: '/', icon: 'overview', description: 'Operational snapshot of your network.' },
      { label: 'Deliveries', path: '/deliveries', icon: 'truck', description: 'Plan, dispatch and follow every delivery.' },
      { label: 'Operations Map', path: '/map', icon: 'map', description: 'Warehouses, distribution points and fleet on a map.' },
      { label: 'Inventory', path: '/inventory', icon: 'box', description: 'Stock levels and movements per warehouse.' },
      { label: 'Risk Alerts', path: '/risk-alerts', icon: 'alert', description: 'Detected risks that may disrupt operations.' },
    ],
  },
  {
    title: 'Intelligence',
    items: [
      { label: 'AI Assistant', path: '/assistant', icon: 'sparkles', description: 'Ask questions about your operations in natural language.' },
    ],
  },
  {
    title: 'Workspace',
    items: [
      { label: 'Settings', path: '/settings', icon: 'settings', description: 'Organisation, users and preferences.' },
    ],
  },
]

export const navItems: NavItem[] = navSections.flatMap((section) => section.items)

export function findNavItem(pathname: string): NavItem | undefined {
  return navItems.find((item) => item.path === pathname)
}
