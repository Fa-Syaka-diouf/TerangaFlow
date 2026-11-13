import type { DatabaseHealthResponse, HealthResponse } from '../types/api'
import { apiClient } from './apiClient'

export const healthService = {
  getApiHealth: (signal?: AbortSignal) => apiClient.get<HealthResponse>('/health', signal),
  getDatabaseHealth: (signal?: AbortSignal) =>
    apiClient.get<DatabaseHealthResponse>('/health/database', signal),
}
