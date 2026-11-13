import { createBrowserRouter, RouterProvider } from 'react-router'
import { AppLayout } from './components/layout/AppLayout'
import { navItems } from './components/layout/navigation'
import { NotFoundPage } from './pages/NotFoundPage'
import { OverviewPage } from './pages/OverviewPage'
import { PlaceholderPage } from './pages/PlaceholderPage'

const router = createBrowserRouter([
  {
    path: '/',
    element: <AppLayout />,
    children: [
      { index: true, element: <OverviewPage /> },
      ...navItems
        .filter((item) => item.path !== '/')
        .map((item) => ({ path: item.path.slice(1), element: <PlaceholderPage item={item} /> })),
      { path: '*', element: <NotFoundPage /> },
    ],
  },
])

export default function App() {
  return <RouterProvider router={router} />
}
