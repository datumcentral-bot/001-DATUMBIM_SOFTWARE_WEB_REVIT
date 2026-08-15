import * as THREE from 'three'
import { SceneManager } from './SceneManager'
import { CameraManager } from './CameraManager'
import { RendererManager } from './RendererManager'
import { ControlsManager } from './ControlsManager'
import { SelectionManager } from './SelectionManager'
import { ModelManager } from './ModelManager'
import { GridManager } from './GridManager'
import { LightingManager } from './LightingManager'
import type { ViewerContext, ViewerOptions, ViewerState, RenderMode, ViewerBIMElement, SelectionHighlightState, ViewerModelReference } from './types/ViewerTypes'
import { DesignEngine } from '@/lib/design/DesignEngine'
import { SelectionEngine } from '@/lib/design/SelectionEngine'
import type { BIMModel } from './adapters/FormatAdapters'
import { DemoModelBuilder } from './demo/DemoModel'

export class ViewerEngine {
  private sceneManager = new SceneManager()
  private cameraManager = new CameraManager()
  private rendererManager = new RendererManager()
  private controlsManager = new ControlsManager()
  private selectionManager = new SelectionManager()
  private modelManager = new ModelManager()
  private gridManager = new GridManager()
  private lightingManager = new LightingManager()
  private context: ViewerContext | null = null
  private designEngine: DesignEngine | null = null
  private animationFrameId: number | null = null
  private state: ViewerState = {
    initialized: false,
    activeViewId: null,
    renderMode: 'shaded',
    cameraMode: 'perspective',
    selection: { selectedIds: [], hoveredId: null, highlightLevel: 'medium' },
    model: null,
    error: null,
  }
  private listeners: Set<(state: ViewerState) => void> = new Set()

  attachDesignEngine(engine: DesignEngine): void {
    this.designEngine = engine
    const selectionEngine = engine.selectionEngine as unknown as SelectionEngine
    this.selectionManager.setSelectionEngine(selectionEngine)
    this.selectionManager.subscribe((sel) => {
      this.state = { ...this.state, selection: sel }
      this.listeners.forEach((listener) => listener(this.state))
      this.updateSelectionVisuals()
    })
  }

  initialize(container: HTMLElement, options: ViewerOptions = {}): ViewerContext {
    if (this.state.initialized) {
      return this.context!
    }
    const width = container.clientWidth || 800
    const height = container.clientHeight || 600
    const context: ViewerContext = {
      width,
      height,
      pixelRatio: options.pixelRatio ?? Math.min(window.devicePixelRatio, 2),
      viewId: 'view-3d',
      container,
    }
    this.context = context

    this.rendererManager.initialize(context)
    this.sceneManager.setBackground(options.background ?? 0x1a1a1a)
    this.lightingManager.attach(this.sceneManager.getScene())
    this.gridManager.attach(this.sceneManager.getScene(), 200, 40)
    this.cameraManager.initialize(width, height)
    const camera = this.cameraManager.getActive() as THREE.PerspectiveCamera
    this.controlsManager.initialize({
      width,
      height,
      pixelRatio: options.pixelRatio ?? Math.min(window.devicePixelRatio, 2),
      viewId: 'view-3d',
      container,
      camera: camera as unknown as THREE.PerspectiveCamera,
    })
    this.modelManager.initialize(this.sceneManager.getScene())

    this.attachEventListeners(container)

    this.state = {
      ...this.state,
      initialized: true,
      activeViewId: context.viewId,
      error: null,
    }

    this.startRenderLoop()

    return context
  }

  getState(): ViewerState {
    return this.state
  }

  subscribe(listener: (state: ViewerState) => void): () => void {
    this.listeners.add(listener)
    return () => this.listeners.delete(listener)
  }

  private attachEventListeners(container: HTMLElement): void {
    const handleClick = (event: MouseEvent) => {
      if (!this.cameraManager.getActive() || !this.modelManager.getRoot()) return
      const picked = this.selectionManager.pick(
        container,
        event.clientX,
        event.clientY,
        this.cameraManager.getActive()!,
        this.modelManager.getRecursiveObjects()
      )
      this.selectionManager.selectObject(picked ? (picked.threeObject as unknown as THREE.Object3D) : null, event.shiftKey)
    }

    const handleMouseMove = (event: MouseEvent) => {
      if (!this.cameraManager.getActive() || !this.modelManager.getRoot()) return
      const picked = this.selectionManager.pick(
        container,
        event.clientX,
        event.clientY,
        this.cameraManager.getActive()!,
        this.modelManager.getRecursiveObjects()
      )
      this.selectionManager.setHovered(picked?.id ?? null)
    }

    container.addEventListener('click', handleClick)
    container.addEventListener('mousemove', handleMouseMove)
    this._cleanupListeners = () => {
      container.removeEventListener('click', handleClick)
      container.removeEventListener('mousemove', handleMouseMove)
    }
  }

  private _cleanupListeners: (() => void) | null = null

  private startRenderLoop(): void {
    const render = () => {
      if (!this.state.initialized) return
      this.animationFrameId = requestAnimationFrame(render)
      this.controlsManager.update()
      const scene = this.sceneManager.getScene()
      const camera = this.cameraManager.getActive()
      if (scene && camera) {
        this.rendererManager.render(scene, camera)
      }
    }
    render()
  }

  loadDemoModel(): BIMModel {
    const model = DemoModelBuilder.build()
    this.modelManager.setModel(model)
    this.fitToView()
    this.state = { ...this.state, model: this.modelManager.getModel() }
    this.listeners.forEach((listener) => listener(this.state))
    return model
  }

  loadModel(adapter: { loadModel: (data: unknown) => BIMModel }, data: unknown): ViewerModelReference {
    const model = this.modelManager.loadModel(adapter, data)
    this.fitToView()
    this.state = { ...this.state, model }
    this.listeners.forEach((listener) => listener(this.state))
    return model
  }

  setRenderMode(mode: RenderMode): void {
    this.state = { ...this.state, renderMode: mode }
    this.applyRenderMode()
    this.listeners.forEach((listener) => listener(this.state))
  }

  private applyRenderMode(): void {
    const mode = this.state.renderMode
    const scene = this.sceneManager.getScene()
    if (!scene) return
    scene.traverse((child) => {
      if (child instanceof THREE.Mesh) {
        if (mode === 'wireframe') {
          child.material = new THREE.MeshBasicMaterial({ color: child.material.color, wireframe: true })
        } else {
          const material = child.material as THREE.MeshStandardMaterial
          material.wireframe = false
        }
      }
    })
  }

  fitToView(): void {
    if (!this.modelManager.getRoot()) return
    const box = new THREE.Box3().setFromObject(this.modelManager.getRoot()!)
    const center = box.getCenter(new THREE.Vector3())
    const size = box.getSize(new THREE.Vector3())
    const maxDim = Math.max(size.x, size.y, size.z)
    const distance = maxDim / (2 * Math.tan((this.cameraManager.getActive() as THREE.PerspectiveCamera).fov * Math.PI / 360))
    const camera = this.cameraManager.getActive()!
    camera.position.set(center.x + distance, center.y + distance, center.z + distance)
    camera.lookAt(center)
    this.controlsManager.getControls()?.target.copy(center)
  }

  setCameraOrientation(direction: 'top' | 'bottom' | 'front' | 'back' | 'left' | 'right'): void {
    if (!this.modelManager.getRoot()) return
    const box = new THREE.Box3().setFromObject(this.modelManager.getRoot()!)
    const center = box.getCenter(new THREE.Vector3())
    const size = box.getSize(new THREE.Vector3())
    const distance = Math.max(size.x, size.y, size.z) * 1.5
    const camera = this.cameraManager.getActive()!
    const positions: Record<string, { x: number; y: number; z: number }> = {
      top: { x: center.x, y: center.y + distance, z: center.z },
      bottom: { x: center.x, y: center.y - distance, z: center.z },
      front: { x: center.x, y: center.y, z: center.z + distance },
      back: { x: center.x, y: center.y, z: center.z - distance },
      left: { x: center.x - distance, y: center.y, z: center.z },
      right: { x: center.x + distance, y: center.y, z: center.z },
    }
    const pos = positions[direction]
    camera.position.set(pos.x, pos.y, pos.z)
    camera.lookAt(center)
    this.controlsManager.getControls()?.target.copy(center)
  }

  private updateSelectionVisuals(): void {
    const selectedIds = this.state.selection.selectedIds
    this.modelManager.getElements().forEach((element) => {
      const mesh = element.threeObject as THREE.Mesh
      if (!mesh.material) return
      if (selectedIds.includes(element.id)) {
        mesh.material = new THREE.MeshStandardMaterial({
          color: 0xffcc00,
          opacity: 1,
          roughness: 0.3,
          metalness: 0.2,
          transparent: false,
        })
      } else {
        const original = this.modelManager.getViewerMaterial(element.materialId)
        if (original) {
          mesh.material = new THREE.MeshStandardMaterial({
            color: original.color,
            opacity: original.opacity,
            roughness: original.roughness,
            metalness: original.metalness,
            transparent: original.transparent,
          })
        }
      }
    })
  }

  resize(width: number, height: number): void {
    this.rendererManager.resize(width, height)
    this.cameraManager.resize(width, height)
  }

  getControls() {
    return this.controlsManager.getControls()
  }

  getScene(): THREE.Scene | null {
    return this.sceneManager.getScene()
  }

  getCamera() {
    return this.cameraManager.getActive()
  }

  getModelManager() {
    return this.modelManager
  }

  getSelectionManager() {
    return this.selectionManager
  }

  getBIMElementMetadata(id: string): Record<string, unknown> | null {
    const element = this.modelManager.getElement(id)
    if (!element) return null
    return {
      id: element.id,
      category: element.category,
      family: element.family,
      type: element.type,
      level: element.level,
      name: element.name,
      visible: element.visible,
      materialId: element.materialId,
      source: element.source,
      modelId: element.modelId,
      metadata: element.metadata,
    }
  }

  dispose(): void {
    if (this.animationFrameId !== null) {
      cancelAnimationFrame(this.animationFrameId)
      this.animationFrameId = null
    }
    this._cleanupListeners?.()
    this.controlsManager.dispose()
    this.rendererManager.dispose()
    this.gridManager.detach()
    this.lightingManager.detach()
    this.modelManager.dispose()
    this.cameraManager.dispose()
    this.sceneManager.dispose()
    this.state = {
      initialized: false,
      activeViewId: null,
      renderMode: 'shaded',
      cameraMode: 'perspective',
      selection: { selectedIds: [], hoveredId: null, highlightLevel: 'medium' },
      model: null,
      error: null,
    }
  }
}
