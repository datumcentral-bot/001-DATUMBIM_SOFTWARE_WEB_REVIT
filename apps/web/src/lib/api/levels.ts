import { apiClient } from '@/lib/apiClient'

export interface LevelResponse {
  id: string
  project_id: string
  name: string
  elevation: number
  height?: number
  is_structural: boolean
  is_ground: boolean
  created_at?: string
  updated_at?: string
}

export const levelApi = {
  async list(projectId: string) {
    const res = await apiClient.get<LevelResponse[]>(`/levels/?project_id=${encodeURIComponent(projectId)}`)
    return res
  },

  async get(id: string) {
    const res = await apiClient.get<LevelResponse>(`/levels/${id}`)
    return res
  },

  async create(payload: { project_id: string; name: string; elevation: number; height?: number; is_structural?: boolean; is_ground?: boolean }) {
    const res = await apiClient.post<LevelResponse>('/levels/', payload)
    return res
  },

  async update(id: string, payload: Partial<{ name: string; elevation: number; height: number; is_structural: boolean; is_ground: boolean }>) {
    const res = await apiClient.put<LevelResponse>(`/levels/${id}`, payload)
    return res
  },

  async remove(id: string) {
    const res = await apiClient.delete<{ detail: string }>(`/levels/${id}`)
    return res
  },
}
