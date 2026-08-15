export interface TransformState {
  position: { x: number; y: number; z: number }
  rotation: { x: number; y: number; z: number }
  scale: { x: number; y: number; z: number }
}

export interface TransformDelta {
  positionDelta?: { x: number; y: number; z: number }
  rotationDelta?: { x: number; y: number; z: number }
  scaleDelta?: { x: number; y: number; z: number }
}

export interface TransformEngineState {
  transforms: Map<string, TransformState>
  pendingDeltas: Map<string, TransformDelta>
  history: TransformHistoryEntry[]
}

export interface TransformHistoryEntry {
  elementId: string
  timestamp: number
  delta: TransformDelta
  previousState: TransformState
}
