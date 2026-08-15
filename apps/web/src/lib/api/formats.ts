import { apiClient } from '@/lib/apiClient'

export interface FormatInfo {
  format: string
  category: string
  extensions: string[]
  mime_types: string[]
}

export interface FormatDetectionResponse {
  format: string
  category: string
  confidence: number
  mime_type?: string
  metadata: Record<string, unknown>
}

export interface FormatUploadResponse {
  file_id: string
  filename: string
  format: string
  category: string
  confidence: number
  size: number
  document_id?: string
  preview?: string
}

export interface FormatImportResponse {
  success: boolean
  format: string
  elements_imported: number
  errors: string[]
  warnings: string[]
  metadata: Record<string, unknown>
}

export const formatApi = {
  async list() {
    const res = await apiClient.get<{ formats: FormatInfo[] }>('/format/formats')
    return res
  },

  async detect(filename: string, contentType?: string) {
    const params = new URLSearchParams({ filename })
    if (contentType) params.set('content_type', contentType)
    const res = await apiClient.get<FormatDetectionResponse>(`/format/detect?${params.toString()}`)
    return res
  },

  async upload(file: File, projectId?: string) {
    const form = new FormData()
    form.append('file', file)
    if (projectId) form.append('project_id', projectId)
    const res = await apiClient.post<FormatUploadResponse>('/format/upload', form)
    return res
  },

  async import(formatName: string, fileId: string, projectId?: string) {
    const params = new URLSearchParams({ format_name: formatName, file_id: fileId })
    if (projectId) params.set('project_id', projectId)
    const res = await apiClient.post<FormatImportResponse>(`/format/import/${encodeURIComponent(formatName)}?${params.toString()}`)
    return res
  },
}
