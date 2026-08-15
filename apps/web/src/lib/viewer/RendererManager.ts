import * as THREE from 'three'
import type { ViewerContext } from './types/ViewerTypes'

export class RendererManager {
  private renderer: THREE.WebGLRenderer | null = null
  private context: ViewerContext | null = null

  initialize(context: ViewerContext): THREE.WebGLRenderer {
    this.context = context
    const container = context.container
    if (!container) {
      throw new Error('Viewer container is required')
    }
    this.renderer = new THREE.WebGLRenderer({ antialias: context.antialias ?? true, alpha: context.alpha ?? false })
    this.renderer.setPixelRatio(context.pixelRatio ?? Math.min(window.devicePixelRatio, 2))
    this.renderer.setSize(context.width, context.height)
    this.renderer.setClearColor(context.background ?? 0x1a1a1a)
    this.renderer.shadowMap.enabled = false
    container.appendChild(this.renderer.domElement)
    return this.renderer
  }

  getRenderer(): THREE.WebGLRenderer | null {
    return this.renderer
  }

  resize(width: number, height: number): void {
    if (!this.renderer || !this.context) return
    this.renderer.setSize(width, height)
    this.renderer.setPixelRatio(this.context.pixelRatio ?? Math.min(window.devicePixelRatio, 2))
  }

  render(scene: THREE.Scene, camera: THREE.Camera): void {
    this.renderer?.render(scene, camera)
  }

  dispose(): void {
    if (this.renderer) {
      if (this.context?.container && this.renderer.domElement.parentNode === this.context.container) {
        this.context.container.removeChild(this.renderer.domElement)
      }
      this.renderer.dispose()
      this.renderer = null
    }
    this.context = null
  }
}
