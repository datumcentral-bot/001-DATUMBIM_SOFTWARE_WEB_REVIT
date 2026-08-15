import { ViewEngineState, ViewDefinition, CameraState } from './types/ViewTypes'

export class ViewEngine {
  private state: ViewEngineState = {
    views: [],
    activeViewId: null,
    cameraState: null,
  }

  private listeners: Set<() => void> = new Set()

  getState(): ViewEngineState {
    return this.state
  }

  subscribe(listener: () => void): () => void {
    this.listeners.add(listener)
    return () => this.listeners.delete(listener)
  }

  private notify(): void {
    this.listeners.forEach((listener) => listener())
  }

  registerView(view: ViewDefinition): void {
    const existing = this.state.views.find((v) => v.id === view.id)
    if (existing) {
      Object.assign(existing, view)
    } else {
      this.state.views.push(view)
    }
    this.notify()
  }

  unregisterView(viewId: string): void {
    this.state.views = this.state.views.filter((v) => v.id !== viewId)
    if (this.state.activeViewId === viewId) {
      this.state.activeViewId = null
      this.state.cameraState = null
    }
    this.notify()
  }

  setActiveView(viewId: string): void {
    const view = this.state.views.find((v) => v.id === viewId)
    if (!view) {
      throw new Error(`View not found: ${viewId}`)
    }
    this.state.activeViewId = viewId
    this.state.cameraState = view.cameraState ?? null
    this.notify()
  }

  getActiveView(): ViewDefinition | null {
    if (!this.state.activeViewId) return null
    return this.state.views.find((v) => v.id === this.state.activeViewId) ?? null
  }

  updateCameraState(cameraState: Partial<CameraState>): void {
    if (!this.state.cameraState) {
      this.state.cameraState = {
        position: { x: 0, y: 0, z: 0 },
        target: { x: 0, y: 0, z: 0 },
        up: { x: 0, y: 1, z: 0 },
      }
    }
    this.state.cameraState = {
      ...this.state.cameraState,
      ...cameraState,
    }
    this.notify()
  }

  getViewsByType(type: ViewDefinition['type']): ViewDefinition[] {
    return this.state.views.filter((v) => v.type === type)
  }

  getViewsByDiscipline(discipline: ViewDefinition['discipline']): ViewDefinition[] {
    return this.state.views.filter((v) => v.discipline === discipline)
  }
}
