import { useState } from 'react'
import { Outlet } from 'react-router'
import { Header } from './Header'
import { Sidebar } from './Sidebar'

export function AppLayout() {
  const [navOpen, setNavOpen] = useState(false)

  return (
    <div className="min-h-screen bg-surface">
      <Sidebar open={navOpen} onClose={() => setNavOpen(false)} />
      <div className="lg:pl-68">
        <Header onOpenNavigation={() => setNavOpen(true)} />
        <main className="mx-auto w-full max-w-[1440px] px-4 py-6 sm:px-6 lg:px-8 lg:py-8">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
