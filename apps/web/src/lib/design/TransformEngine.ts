import { TransformEngineState, TransformDelta, TransformState, TransformHistoryEntry } from './types/TransformTypes'

export class TransformEngine {
  private state: TransformEngineState = {
    transforms: new Map(),
    pendingDeltas: new Map(),
    history: [],
  }

  private listeners: Set<() => void> = new Set()

  getState(): TransformEngineState {
    return this.state
  }

  subscribe(listener: () => void): () => void {
    this.listeners.add(listener)
    return () => this.listeners.delete(listener)
  }

  private notify(): void {
    this.listeners.forEach((listener) => listener())
  }

  registerTransform(id: string, transform: TransformState): void {
    this.state.transforms.set(id, transform)
    this.notify()
  }

  getTransform(id: string): TransformState | undefined {
    return this.state.transforms.get(id)
  }

  updateTransform(id: string, delta: TransformDelta): void {
    const existing = this.state.transforms.get(id)
    if (!existing) {
      throw new Error(`Transform not found: ${id}`)
    }

    const previousState = { ...existing }
    const newState: TransformState = {
      position: {
        x: existing.position.x + (delta.positionDelta?.x ?? 0),
        y: existing.position.y + (delta.positionDelta?.y ?? 0),
        z: existing.position.z + (delta.positionDelta?.z ?? 0),
      },
      rotation: {
        x: existing.rotation.x + (delta.rotationDelta?.x ?? 0),
        y: existing.rotation.y + (delta.rotationDelta?.y ?? 0),
        z: existing.rotation.z + (delta.rotationDelta?.z ?? 0),
      },
      scale: {
        x: existing.scale.x + (delta.scaleDelta?.x ?? 0),
        y: existing.scale.y + (delta.scaleDelta?.y ?? 0),
        z: existing.scale.z + (delta.scaleDelta?.z ?? 0),
      },
    }

    this.state.transforms.set(id, newState)
    this.state.history.push({
      elementId: id,
      timestamp: Date.now(),
      delta,
      previousState,
    })
    this.notify()
  }

  applyDelta(id: string, delta: TransformDelta): void {
    this.state.pendingDeltas.set(id, delta)
    this.notify()
  }

  commitPending(id: string): void {
    const delta = this.state.pendingDeltas.get(id)
    if (delta) {
      this.updateTransform(id, delta)
      this.state.pendingDeltas.delete(id)
    }
  }

  rollbackPending(id: string): void {
    this.state.pendingDeltas.delete(id)
    this.notify()
  }

  undoLast(): TransformHistoryEntry | undefined {
    return this.state.history.pop()
  }

  reset(id: string): void {
    this.state.transforms.delete(id)
    this.state.pendingDeltas.delete(id)
    this.notify()
  }
}
