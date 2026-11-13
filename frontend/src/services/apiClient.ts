import type { ApiErrorBody } from '../types/api'
import { env } from '../utils/env'

/** Error raised for any failed API call (network, timeout or HTTP status). */
export class ApiError extends Error {
  readonly status: number
  readonly code: string
  readonly details?: unknown

  constructor(message: string, status: number, code: string, details?: unknown) {
    super(message)
    this.name = 'ApiError'
    this.status = status
    this.code = code
    this.details = details
  }
}

type HttpMethod = 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE'

interface RequestOptions {
  method?: HttpMethod
  body?: unknown
  signal?: AbortSignal
  headers?: Record<string, string>
}

function isApiErrorBody(value: unknown): value is ApiErrorBody {
  if (typeof value !== 'object' || value === null || !('error' in value)) return false
  const { error } = value as { error: unknown }
  return typeof error === 'object' && error !== null && typeof (error as { message?: unknown }).message === 'string'
}

export function isAbortError(error: unknown): boolean {
  return error instanceof DOMException && error.name === 'AbortError'
}

/**
 * Thin wrapper around `fetch`: base URL, JSON (de)serialisation,
 * timeout and normalised errors. No external HTTP dependency needed.
 */
export async function apiRequest<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const { method = 'GET', body, signal, headers } = options
  const timeoutSignal = AbortSignal.timeout(env.apiTimeoutMs)
  const combinedSignal = signal ? AbortSignal.any([signal, timeoutSignal]) : timeoutSignal

  let response: Response
  try {
    response = await fetch(`${env.apiBaseUrl}${path}`, {
      method,
      headers: {
        Accept: 'application/json',
        ...(body !== undefined ? { 'Content-Type': 'application/json' } : {}),
        ...headers,
      },
      body: body !== undefined ? JSON.stringify(body) : undefined,
      signal: combinedSignal,
    })
  } catch (cause) {
    if (isAbortError(cause)) throw cause
    if (cause instanceof DOMException && cause.name === 'TimeoutError') {
      throw new ApiError('The API did not respond in time.', 0, 'timeout')
    }
    throw new ApiError('Unable to reach the API.', 0, 'network_error')
  }

  const payload: unknown = response.status === 204 ? null : await response.json().catch(() => null)

  if (!response.ok) {
    if (isApiErrorBody(payload)) {
      throw new ApiError(payload.error.message, response.status, payload.error.code, payload.error.details)
    }
    throw new ApiError(`Request failed with status ${response.status}.`, response.status, 'http_error')
  }

  return payload as T
}

export const apiClient = {
  get: <T>(path: string, signal?: AbortSignal) => apiRequest<T>(path, { signal }),
  post: <T>(path: string, body: unknown, signal?: AbortSignal) =>
    apiRequest<T>(path, { method: 'POST', body, signal }),
}
