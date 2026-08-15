import { apiClient } from '@/lib/apiClient'

export interface DocumentResponse {
  id: string
  project_id: string
  name: string
  description?: string
  file_path?: string
  file_format?: string
  file_size?: number
  version?: string
  revision?: string
  status?: string
  created_at?: string
  updated_at?: string
}

export const documentApi = {
  async list(projectId: string) {
    const res = await apiClient.get<DocumentResponse[]>(`/documents/?project_id=${encodeURIComponent(projectId)}`)
    return res
  },

  async get(id: string) {
    const res = await apiClient.get<DocumentResponse>(`/documents/${id}`)
    return res
  },

  async create(payload: { project_id: string; name: string; description?: string; file_path?: string; file_format?: string; version?: string; revision?: string; status?: string }) {
    const res = await apiClient.post<DocumentResponse>('/documents/', payload)
    return res
  },

  async update(id: string, payload: Partial<{ name: string; description: string; file_path: string; file_format: string; version: string; revision: string; status: string }>) {
    const res = await apiClient.put<DocumentResponse>(`/documents/${id}`, payload)
    return res
  },

  async remove(id: string) {
    const res = await apiClient.delete<{ detail: string }>(`/documents/${id}`)
    return res
  },
}
