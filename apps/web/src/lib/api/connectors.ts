import { apiClient } from '@/lib/apiClient'
import type { ApplicationConnector, ApplicationSession } from '@/lib/connectors/types/ConnectorTypes'

export interface ConnectorsResponse {
  connectors: ApplicationConnector[]
}

export interface SessionsResponse {
  sessions: ApplicationSession[]
}

export const connectorsApi = {
  async list(status?: string): Promise<ApplicationConnector[]> {
    const endpoint = status ? `/connectors?status=${encodeURIComponent(status)}` : '/connectors'
    const response = await apiClient.get<{ connectors: ApplicationConnector[] }>(endpoint)
    return response.data?.connectors ?? []
  },

  async get(connectorId: string): Promise<ApplicationConnector | null> {
    const response = await apiClient.get<{ connector: ApplicationConnector }>(`/connectors/${connectorId}`)
    return response.data?.connector ?? null
  },

  async connect(connectorId: string): Promise<ApplicationSession | null> {
    const response = await apiClient.post<{ session: ApplicationSession }>(`/connectors/${connectorId}/connect`)
    return response.data?.session ?? null
  },

  async disconnect(connectorId: string, sessionId: string): Promise<void> {
    await apiClient.delete<{ status: string }>(`/connectors/${connectorId}/sessions/${sessionId}`)
  },

  async listSessions(): Promise<ApplicationSession[]> {
    const response = await apiClient.get<{ sessions: ApplicationSession[] }>('/connectors/sessions')
    return response.data?.sessions ?? []
  },

  async getSession(sessionId: string): Promise<ApplicationSession | null> {
    const response = await apiClient.get<{ session: ApplicationSession }>(`/connectors/sessions/${sessionId}`)
    return response.data?.session ?? null
  },
}
