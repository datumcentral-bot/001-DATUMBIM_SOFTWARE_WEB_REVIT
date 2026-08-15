import { ViewEngine } from './ViewEngine'
import { ElementEngine } from './ElementEngine'
import { SelectionEngine } from './SelectionEngine'
import { TransformEngine } from './TransformEngine'
import { RenderEngine } from './RenderEngine'

export interface DesignEngineState {
  initialized: boolean
  activeViewId: string | null
  selectedElementIds: string[]
  renderContext: { width: number; height: number; pixelRatio: number } | null
}

export class DesignEngine {
  public readonly viewEngine: ViewEngine
  public readonly elementEngine: ElementEngine
  public readonly selectionEngine: SelectionEngine
  public readonly transformEngine: TransformEngine
  public readonly renderEngine: RenderEngine

  private initialized: boolean = false
  private listeners: Set<() => void> = new Set()

  constructor() {
    this.viewEngine = new ViewEngine()
    this.elementEngine = new ElementEngine()
    this.selectionEngine = new SelectionEngine()
    this.transformEngine = new TransformEngine()
    this.renderEngine = new RenderEngine()
  }

  getState(): DesignEngineState {
    return {
      initialized: this.initialized,
      activeViewId: this.viewEngine.getState().activeViewId,
      selectedElementIds: this.selectionEngine.getState().selectedIds,
      renderContext: this.renderEngine.getContext() ?? null,
    }
  }

  subscribe(listener: () => void): () => void {
    this.listeners.add(listener)
    return () => this.listeners.delete(listener)
  }

  private notify(): void {
    this.listeners.forEach((listener) => listener())
  }

  initialize(): void {
    if (this.initialized) return
    this.initialized = true
    this.notify()
  }

  dispose(): void {
    this.renderEngine.dispose()
    this.initialized = false
    this.notify()
  }

  isInitialized(): boolean {
    return this.initialized
  }
}
