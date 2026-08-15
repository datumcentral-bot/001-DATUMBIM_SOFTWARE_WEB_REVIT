import * as THREE from 'three'
import type { ViewerBIMElement, SelectionHighlightState } from './types/ViewerTypes'
import type { SelectionEngine } from '@/lib/design/SelectionEngine'

export class SelectionManager {
  private raycaster: THREE.Raycaster = new THREE.Raycaster()
  private mouse: THREE.Vector2 = new THREE.Vector2()
  private selectionEngine: SelectionEngine | null = null
  private elementMap: Map<THREE.Object3D, ViewerBIMElement> = new Map()
  private state: SelectionHighlightState = {
    selectedIds: [],
    hoveredId: null,
    highlightLevel: 'medium',
  }
  private listeners: Set<(state: SelectionHighlightState) => void> = new Set()

  setSelectionEngine(engine: SelectionEngine): void {
    this.selectionEngine = engine
    engine.subscribe(() => this.syncFromEngine())
  }

  registerElement(element: ViewerBIMElement): void {
    this.elementMap.set(element.threeObject as unknown as THREE.Object3D, element)
  }

  unregisterElement(element: ViewerBIMElement): void {
    this.elementMap.delete(element.threeObject as unknown as THREE.Object3D)
  }

  getElementByObject(object: THREE.Object3D): ViewerBIMElement | undefined {
    return this.elementMap.get(object)
  }

  getState(): SelectionHighlightState {
    return this.state
  }

  subscribe(listener: (state: SelectionHighlightState) => void): () => void {
    this.listeners.add(listener)
    return () => this.listeners.delete(listener)
  }

  pick(container: HTMLElement, clientX: number, clientY: number, camera: THREE.Camera, recursiveObjects: THREE.Object3D[]): ViewerBIMElement | null {
    const rect = container.getBoundingClientRect()
    this.mouse.x = ((clientX - rect.left) / rect.width) * 2 - 1
    this.mouse.y = -((clientY - rect.top) / rect.height) * 2 + 1
    this.raycaster.setFromCamera(this.mouse, camera)
    const intersects = this.raycaster.intersectObjects(recursiveObjects, false)
    if (intersects.length > 0) {
      const hit = intersects[0].object
      return this.elementMap.get(hit) || null
    }
    return null
  }

  selectObject(object: THREE.Object3D | null, additive = false): void {
    if (!object) {
      this.clearSelection()
      return
    }
    const element = this.elementMap.get(object)
    if (!element) return
    if (!this.selectionEngine) return
    this.selectionEngine.select(element.id, additive)
  }

  clearSelection(): void {
    if (!this.selectionEngine) return
    this.selectionEngine.clearSelection()
  }

  private syncFromEngine(): void {
    if (!this.selectionEngine) return
    const ids = this.selectionEngine.getState().selectedIds
    this.state = { ...this.state, selectedIds: [...ids] }
    this.listeners.forEach((listener) => listener(this.state))
  }

  setHovered(id: string | null): void {
    this.state = { ...this.state, hoveredId: id }
    this.listeners.forEach((listener) => listener(this.state))
  }
}
