import { create } from 'zustand'
import { DesignEngine } from '@/lib/design'
import { ViewerEngine } from '@/lib/viewer'

export interface DesignSliceState {
  engine: DesignEngine
  initialized: boolean
  initialize: () => void
  dispose: () => void
  selectElement: (id: string, additive?: boolean) => void
  clearSelection: () => void
  setActiveView: (viewId: string) => void
  updateCameraState: (state: { position?: { x: number; y: number; z: number }; target?: { x: number; y: number; z: number }; up?: { x: number; y: number; z: number } }) => void
  zoomExtents: () => void
  zoomIn: () => void
  zoomOut: () => void
  fitToView: () => void
  getSelectedElements: () => string[]
  getActiveView: () => ReturnType<DesignEngine['viewEngine']['getActiveView']>
  setViewerEngine: (engine: ViewerEngine | null) => void
  getViewerEngine: () => ViewerEngine | null
  loadDemoModel: () => void
  setRenderMode: (mode: 'shaded' | 'wireframe') => void
}

export const useDesignSlice = create<DesignSliceState>((set, get) => ({
  engine: new DesignEngine(),
  initialized: false,

  initialize: () => {
    const { engine } = get()
    engine.initialize()
    set({ initialized: true })
  },

  dispose: () => {
    const { engine } = get()
    engine.dispose()
    set({ initialized: false })
  },

  selectElement: (id: string, additive = false) => {
    const { engine } = get()
    engine.selectionEngine.select(id, additive)
  },

  clearSelection: () => {
    const { engine } = get()
    engine.selectionEngine.clearSelection()
  },

  setActiveView: (viewId: string) => {
    const { engine } = get()
    engine.viewEngine.setActiveView(viewId)
  },

  updateCameraState: (cameraState) => {
    const { engine } = get()
    engine.viewEngine.updateCameraState(cameraState)
  },

  zoomExtents: () => {
    const { engine } = get()
    engine.viewEngine.updateCameraState({ position: { x: 100, y: 100, z: 100 }, target: { x: 0, y: 0, z: 0 } })
  },

  zoomIn: () => {
    const { engine } = get()
    const current = engine.viewEngine.getState().cameraState
    if (!current) return
    const direction = {
      x: current.target.x - current.position.x,
      y: current.target.y - current.position.y,
      z: current.target.z - current.position.z,
    }
    const len = Math.sqrt(direction.x ** 2 + direction.y ** 2 + direction.z ** 2)
    if (len === 0) return
    const factor = 0.8
    engine.viewEngine.updateCameraState({
      position: {
        x: current.position.x + direction.x * factor,
        y: current.position.y + direction.y * factor,
        z: current.position.z + direction.z * factor,
      },
    })
  },

  zoomOut: () => {
    const { engine } = get()
    const current = engine.viewEngine.getState().cameraState
    if (!current) return
    const direction = {
      x: current.position.x - current.target.x,
      y: current.position.y - current.target.y,
      z: current.position.z - current.target.z,
    }
    const len = Math.sqrt(direction.x ** 2 + direction.y ** 2 + direction.z ** 2)
    if (len === 0) return
    const factor = 1.25
    engine.viewEngine.updateCameraState({
      position: {
        x: current.position.x + direction.x * factor,
        y: current.position.y + direction.y * factor,
        z: current.position.z + direction.z * factor,
      },
    })
  },

  fitToView: () => {
    get().zoomExtents()
  },

  getSelectedElements: () => {
    const { engine } = get()
    return engine.selectionEngine.getState().selectedIds
  },

  getActiveView: () => {
    const { engine } = get()
    return engine.viewEngine.getActiveView()
  },

  setViewerEngine: (viewerEngine: ViewerEngine | null) => {
    const { engine } = get()
    engine.viewerEngine = viewerEngine
    engine.renderEngine.setViewerEngine(viewerEngine)
  },

  getViewerEngine: () => {
    const { engine } = get()
    return engine.viewerEngine
  },

  loadDemoModel: () => {
    const { engine } = get()
    if (engine.viewerEngine) {
      engine.viewerEngine.loadDemoModel()
    }
  },

  setRenderMode: (mode: 'shaded' | 'wireframe') => {
    const { engine } = get()
    if (engine.viewerEngine) {
      engine.viewerEngine.setRenderMode(mode)
    }
  },
}))
