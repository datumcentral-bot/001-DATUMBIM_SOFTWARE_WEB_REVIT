export interface ViewDefinition {
  id: string
  name: string
  type: '3d' | 'floor-plan' | 'ceiling-plan' | 'elevation' | 'section' | 'detail' | 'schedule' | 'sheet' | 'drafting' | 'browser' | 'model' | 'applications' | 'sessions' | 'observation' | 'control' | 'ai'
  discipline: 'architecture' | 'structure' | 'mep' | 'coordination' | 'generic'
  visibilityState: boolean
  activeState: boolean
  cameraState?: CameraState
  modelReference?: string
}

export interface CameraState {
  position: { x: number; y: number; z: number }
  target: { x: number; y: number; z: number }
  up: { x: number; y: number; z: number }
}

export interface ViewEngineState {
  views: ViewDefinition[]
  activeViewId: string | null
  cameraState: CameraState | null
}
