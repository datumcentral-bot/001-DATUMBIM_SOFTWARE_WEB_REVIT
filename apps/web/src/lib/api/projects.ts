import { apiClient } from '@/lib/apiClient'
import type { ProjectResponse } from '@/types/api'

export const projectApi = {
  async list() {
    const res = await apiClient.get<ProjectResponse[]>('/projects/')
    return res
  },

  async get(id: string) {
    const res = await apiClient.get<ProjectResponse>(`/projects/${id}`)
    return res
  },

  async create(payload: { name: string; description?: string; is_active?: boolean }) {
    const res = await apiClient.post<ProjectResponse>('/projects/', payload)
    return res
  },

  async update(id: string, payload: Partial<{ name: string; description: string; is_active: boolean }>) {
    const res = await apiClient.put<ProjectResponse>(`/projects/${id}`, payload)
    return res
  },

  async remove(id: string) {
    const res = await apiClient.delete<{ detail: string }>(`/projects/${id}`)
    return res
  },

  async models(projectId: string) {
    const res = await apiClient.get(`/projects/${projectId}/models`)
    return res
  },
}
