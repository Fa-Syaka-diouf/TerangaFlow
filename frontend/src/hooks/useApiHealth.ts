import { useEffect, useState } from 'react'
import { isAbortError } from '../services/apiClient'
import { healthService } from '../services/healthService'

export type ApiHealthState = 'checking' | 'online' | 'offline'

/** Pings `GET /health` on mount, then every `intervalMs`. */
export function useApiHealth(intervalMs = 30_000): ApiHealthState {
  const [state, setState] = useState<ApiHealthState>('checking')

  useEffect(() => {
    const controller = new AbortController()

    const check = () => {
      healthService
        .getApiHealth(controller.signal)
        .then(() => setState('online'))
        .catch((error: unknown) => {
          if (!isAbortError(error)) setState('offline')
        })
    }

    check()
    const timer = window.setInterval(check, intervalMs)
    return () => {
      controller.abort()
      window.clearInterval(timer)
    }
  }, [intervalMs])

  return state
}
