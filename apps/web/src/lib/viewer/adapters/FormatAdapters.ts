import * as THREE from 'three'
import type { ViewerMaterial } from '../types/ViewerTypes'

export interface GeometryData {
  type: 'box' | 'plane' | 'cylinder' | 'sphere' | 'line'
  width?: number
  height?: number
  depth?: number
  radiusTop?: number
  radiusBottom?: number
  radius?: number
  points?: Array<{ x: number; y: number; z: number }>
}

export interface MaterialData {
  id: string
  name: string
  color: number
  opacity: number
  roughness: number
  metalness: number
  transparent: boolean
}

export interface TransformData {
  position: { x: number; y: number; z: number }
  rotation: { x: number; y: number; z: number }
  scale: { x: number; y: number; z: number }
}

export interface BIMElement {
  id: string
  category: string
  family: string
  type: string
  level: string
  name: string
  visible: boolean
  geometry: GeometryData
  transform: TransformData
  material: MaterialData
  source: string
  modelId: string
  metadata: Record<string, unknown>
}

export interface BIMModel {
  id: string
  name: string
  elements: BIMElement[]
  materials: MaterialData[]
  geometryLoader: GeometryLoader
}

export interface GeometryLoader {
  loadGeometry(geometry: GeometryData): GeometryData
}

export interface ModelLoader {
  loadModel(data: unknown): BIMModel
}

export interface ViewerMaterialLibrary {
  getMaterial(id: string): ViewerMaterial | undefined
  getMaterials(): ViewerMaterial[]
}
