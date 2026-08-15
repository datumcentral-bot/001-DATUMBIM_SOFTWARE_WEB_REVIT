import { apiClient } from '@/lib/apiClient'

export interface ElementResponse {
  id: string
  project_id?: string
  type_id: string
  category: string
  name: string
  properties?: string
  transform_state?: string
  visibility: boolean
  selection_state: string
  created_at?: string
  updated_at?: string
}

export const elementApi = {
  async list(projectId: string, category?: string) {
    const params = new URLSearchParams({ project_id: projectId })
    if (category) params.set('category', category)
    const res = await apiClient.get<ElementResponse[]>(`/elements/?${params.toString()}`)
    return res
  },

  async get(id: string) {
    const res = await apiClient.get<ElementResponse>(`/elements/${id}`)
    return res
  },

  async create(payload: { project_id: string; type_id: string; category: string; name: string; properties?: string; transform_state?: string; visibility?: boolean; selection_state?: string }) {
    const res = await apiClient.post<ElementResponse>('/elements/', payload)
    return res
  },

  async update(id: string, payload: Partial<{ type_id: string; category: string; name: string; properties: string; transform_state: string; visibility: boolean; selection_state: string }>) {
    const res = await apiClient.put<ElementResponse>(`/elements/${id}`, payload)
    return res
  },

  async remove(id: string) {
    const res = await apiClient.delete<{ detail: string }>(`/elements/${id}`)
    return res
  },
}
