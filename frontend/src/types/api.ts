/** Shape of every error returned by the TerangaFlow API. */
export interface ApiErrorBody {
  error: {
    code: string
    message: string
    details?: unknown
  }
}

export interface HealthResponse {
  status: 'ok'
  service: string
  version: string
  environment: string
  timestamp: string
}

export interface DatabaseHealthResponse {
  status: 'ok' | 'unavailable'
  database: string
  latency_ms: number | null
  detail: string | null
}
