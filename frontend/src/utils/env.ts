/**
 * Centralised, typed access to the Vite environment variables.
 * Values are read once at startup; defaults target local development.
 */
const DEFAULT_API_BASE_URL = 'http://localhost:8000/api/v1'
const DEFAULT_TIMEOUT_MS = 10_000

function parsePositiveInt(value: string | undefined, fallback: number): number {
  const parsed = Number.parseInt(value ?? '', 10)
  return Number.isFinite(parsed) && parsed > 0 ? parsed : fallback
}

export const env = {
  apiBaseUrl: (import.meta.env.VITE_API_BASE_URL || DEFAULT_API_BASE_URL).replace(/\/+$/, ''),
  apiTimeoutMs: parsePositiveInt(import.meta.env.VITE_API_TIMEOUT_MS, DEFAULT_TIMEOUT_MS),
} as const
