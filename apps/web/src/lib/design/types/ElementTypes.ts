import { TransformState } from './TransformTypes'

export interface ElementDefinition {
  id: string
  typeId: string
  category: string
  name: string
  properties: Record<string, unknown>
  transform: TransformState
  visibility: boolean
  selectionState: SelectionState
  metadata: ElementMetadata
}

export interface ElementTypeDefinition {
  id: string
  name: string
  category: string
  properties: PropertyDefinition[]
  baseTransform: TransformState
}

export interface PropertyDefinition {
  key: string
  label: string
  type: 'text' | 'number' | 'boolean' | 'enum' | 'length' | 'area' | 'volume' | 'material' | 'element'
  value: unknown
  readonly?: boolean
  unit?: string
}

export interface ElementMetadata {
  createdBy?: string
  createdAt?: Date
  modifiedBy?: string
  modifiedAt?: Date
  version?: string
  source?: string
}

export interface SelectionState {
  selected: boolean
  highlightLevel: 'none' | 'low' | 'medium' | 'high'
  isolationState: 'none' | 'isolated' | 'hidden'
}
