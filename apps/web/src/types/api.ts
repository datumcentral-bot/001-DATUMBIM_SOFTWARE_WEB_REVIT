export interface ProjectResponse {
  id: string
  name: string
  description?: string
  is_active: boolean
  created_at?: string
  updated_at?: string
}

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
