import { ViewerEngine } from '@/lib/viewer'

export class RenderEngine {
  private initialized: boolean = false
  private context: RenderContext | null = null
  private viewerEngine: ViewerEngine | null = null

  initialize(context: RenderContext): void {
    this.context = context
    this.initialized = true
  }

  isInitialized(): boolean {
    return this.initialized
  }

  getContext(): RenderContext | null {
    return this.context
  }

  setViewerEngine(engine: ViewerEngine | null): void {
    this.viewerEngine = engine
  }

  getViewerEngine(): ViewerEngine | null {
    return this.viewerEngine
  }

  render(): void {
    if (!this.initialized || !this.context) {
      throw new Error('Render engine not initialized')
    }
  }

  resize(width: number, height: number): void {
    if (!this.context) return
    this.context.width = width
    this.context.height = height
    this.viewerEngine?.resize(width, height)
  }

  dispose(): void {
    this.viewerEngine?.dispose()
    this.viewerEngine = null
    this.context = null
    this.initialized = false
  }
}

export interface RenderContext {
  width: number
  height: number
  pixelRatio: number
  viewId: string
}
