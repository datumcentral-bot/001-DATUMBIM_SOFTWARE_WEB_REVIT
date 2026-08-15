import type { CameraState } from '@/lib/design/types/ViewTypes'
import type { PerspectiveCamera } from 'three'

export interface ViewerContext {
  width: number
  height: number
  pixelRatio: number
  viewId: string
  container: HTMLElement | null
  camera?: PerspectiveCamera
  antialias?: boolean
  alpha?: boolean
  background?: number
}

export interface ViewerOptions {
  antialias?: boolean
  alpha?: boolean
  background?: number
  pixelRatio?: number
}

export type RenderMode = 'shaded' | 'wireframe' | 'hidden-line' | 'realistic'

export type Object3DRef = unknown

export interface ViewerBIMElement {
  id: string
  category: string
  family: string
  type: string
  level: string
  name: string
  visible: boolean
  materialId: string
  source: string
  modelId: string
  metadata: Record<string, unknown>
  threeObject: Object3DRef
}

export interface ViewerMaterial {
  id: string
  name: string
  color: number
  opacity: number
  roughness: number
  metalness: number
  transparent: boolean
}

export interface SelectionHighlightState {
  selectedIds: string[]
  hoveredId: string | null
  highlightLevel: 'none' | 'low' | 'medium' | 'high'
}

export interface ViewerModelReference {
  id: string
  name: string
  loaded: boolean
  root: Object3DRef | null
}

export interface ViewerState {
  initialized: boolean
  activeViewId: string | null
  renderMode: RenderMode
  cameraMode: 'perspective' | 'orthographic'
  selection: SelectionHighlightState
  model: ViewerModelReference | null
  error: string | null
}
