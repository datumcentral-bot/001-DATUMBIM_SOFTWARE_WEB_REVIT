import * as THREE from 'three'

export interface BIMGrid {
  id: string
  name: string
  start: { x: number; y: number; z: number }
  end: { x: number; y: number; z: number }
  direction: 'x' | 'y' | 'z'
  elevation: number
  visible: boolean
}

export class BIMGridManager {
  private scene: THREE.Scene | null = null
  private gridGroup: THREE.Group | null = null
  private grids: Map<string, BIMGrid> = new Map()
  private gridObjects: Map<string, THREE.Object3D> = new Map()
  private listeners: Set<(grids: BIMGrid[]) => void> = new Set()

  initialize(scene: THREE.Scene): void {
    this.scene = scene
    this.gridGroup = new THREE.Group()
    this.gridGroup.name = 'BIM-Grids'
    scene.add(this.gridGroup)
  }

  getGrids(): BIMGrid[] {
    return Array.from(this.grids.values())
  }

  getGrid(id: string): BIMGrid | undefined {
    return this.grids.get(id)
  }

  registerGrid(grid: BIMGrid): void {
    this.grids.set(grid.id, grid)
    this.updateGridVisual(grid)
    this.notify()
  }

  registerGrids(grids: BIMGrid[]): void {
    grids.forEach((grid) => {
      this.grids.set(grid.id, grid)
      this.updateGridVisual(grid)
    })
    this.notify()
  }

  setGridVisibility(gridId: string, visible: boolean): void {
    const grid = this.grids.get(gridId)
    if (!grid) return
    grid.visible = visible
    const obj = this.gridObjects.get(gridId)
    if (obj) obj.visible = visible
    this.notify()
  }

  setAllVisibility(visible: boolean): void {
    this.grids.forEach((grid, id) => {
      grid.visible = visible
      const obj = this.gridObjects.get(id)
      if (obj) obj.visible = visible
    })
    this.notify()
  }

  subscribe(listener: (grids: BIMGrid[]) => void): () => void {
    this.listeners.add(listener)
    return () => this.listeners.delete(listener)
  }

  private notify(): void {
    const grids = this.getGrids()
    this.listeners.forEach((listener) => listener(grids))
  }

  private updateGridVisual(grid: BIMGrid): void {
    if (!this.gridGroup || !this.scene) return
    const existing = this.gridObjects.get(grid.id)
    if (existing) {
      this.gridGroup.remove(existing)
    }
    if (!grid.visible) return

    const group = new THREE.Group()
    group.name = `grid-${grid.id}`
    group.visible = grid.visible

    const lineMaterial = new THREE.LineBasicMaterial({
      color: 0x4ade80,
      opacity: 0.8,
      transparent: true,
      depthTest: true,
    })
    const points = [
      new THREE.Vector3(grid.start.x, grid.start.y, grid.start.z),
      new THREE.Vector3(grid.end.x, grid.end.y, grid.end.z),
    ]
    const lineGeometry = new THREE.BufferGeometry().setFromPoints(points)
    const line = new THREE.Line(lineGeometry, lineMaterial)
    line.renderOrder = 1
    group.add(line)

    const labelSprite = this.createLabel(grid.name, grid.end)
    group.add(labelSprite)

    this.gridGroup.add(group)
    this.gridObjects.set(grid.id, group)
  }

  private createLabel(text: string, position: { x: number; y: number; z: number }): THREE.Sprite {
    const canvas = document.createElement('canvas')
    const context = canvas.getContext('2d')
    canvas.width = 256
    canvas.height = 64
    if (context) {
      context.fillStyle = 'rgba(0,0,0,0.5)'
      context.fillRect(0, 0, canvas.width, canvas.height)
      context.font = 'Bold 32px Arial'
      context.fillStyle = '#4ade80'
      context.textAlign = 'center'
      context.textBaseline = 'middle'
      context.fillText(text, canvas.width / 2, canvas.height / 2)
    }
    const texture = new THREE.CanvasTexture(canvas)
    texture.minFilter = THREE.LinearFilter
    texture.magFilter = THREE.LinearFilter
    const material = new THREE.SpriteMaterial({
      map: texture,
      transparent: true,
      depthTest: false,
      depthWrite: false,
    })
    const sprite = new THREE.Sprite(material)
    sprite.position.set(position.x + 500, position.y + 1000, position.z)
    sprite.scale.set(2000, 500, 1)
    sprite.renderOrder = 2
    return sprite
  }

  dispose(): void {
    if (this.gridGroup && this.scene) {
      this.gridObjects.forEach((obj) => {
        this.gridGroup?.remove(obj)
        obj.traverse((child) => {
          if (child instanceof THREE.Line) {
            child.geometry.dispose()
            const materials = Array.isArray(child.material) ? child.material : [child.material]
            materials.forEach((m) => m.dispose())
          }
          if (child instanceof THREE.Sprite) {
            child.material.dispose()
            if (child.material.map) child.material.map.dispose()
          }
        })
      })
      this.scene.remove(this.gridGroup)
    }
    this.grids.clear()
    this.gridObjects.clear()
    this.gridGroup = null
    this.scene = null
  }
}
