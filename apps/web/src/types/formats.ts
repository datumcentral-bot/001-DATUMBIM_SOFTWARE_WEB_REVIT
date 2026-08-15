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
