export class RenderEngine {
  private initialized: boolean = false
  private context: RenderContext | null = null

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

  render(): void {
    if (!this.initialized || !this.context) {
      throw new Error('Render engine not initialized')
    }
  }

  resize(width: number, height: number): void {
    if (!this.context) return
    this.context.width = width
    this.context.height = height
  }

  dispose(): void {
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
