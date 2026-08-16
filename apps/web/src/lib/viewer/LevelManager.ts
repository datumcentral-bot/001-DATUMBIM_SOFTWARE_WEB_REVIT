import * as THREE from 'three'

export interface BIMLevel {
  id: string
  name: string
  elevation: number
  height: number
  visible: boolean
}

export class LevelManager {
  private scene: THREE.Scene | null = null
  private levelGroup: THREE.Group | null = null
  private levels: Map<string, BIMLevel> = new Map()
  private levelObjects: Map<string, THREE.Object3D> = new Map()
  private listeners: Set<(levels: BIMLevel[]) => void> = new Set()

  initialize(scene: THREE.Scene): void {
    this.scene = scene
    this.levelGroup = new THREE.Group()
    this.levelGroup.name = 'BIM-Levels'
    scene.add(this.levelGroup)
  }

  getLevels(): BIMLevel[] {
    return Array.from(this.levels.values())
  }

  getLevel(id: string): BIMLevel | undefined {
    return this.levels.get(id)
  }

  registerLevel(level: BIMLevel): void {
    this.levels.set(level.id, level)
    this.updateLevelVisual(level)
    this.notify()
  }

  setLevelVisibility(levelId: string, visible: boolean): void {
    const level = this.levels.get(levelId)
    if (!level) return
    level.visible = visible
    const obj = this.levelObjects.get(levelId)
    if (obj) obj.visible = visible
    this.notify()
  }

  setActiveLevel(levelId: string): void {
    this.levels.forEach((level, id) => {
      level.visible = id === levelId
      const obj = this.levelObjects.get(id)
      if (obj) obj.visible = id === levelId
    })
    this.notify()
  }

  subscribe(listener: (levels: BIMLevel[]) => void): () => void {
    this.listeners.add(listener)
    return () => this.listeners.delete(listener)
  }

  private notify(): void {
    const levels = this.getLevels()
    this.listeners.forEach((listener) => listener(levels))
  }

  private updateLevelVisual(level: BIMLevel): void {
    if (!this.levelGroup || !this.scene) return
    const existing = this.levelObjects.get(level.id)
    if (existing) {
      this.levelGroup.remove(existing)
    }
    if (!level.visible) return

    const group = new THREE.Group()
    group.name = `level-${level.id}`
    group.visible = level.visible

    const planeGeometry = new THREE.PlaneGeometry(200000, 200000)
    const planeMaterial = new THREE.MeshBasicMaterial({
      color: 0x3a86ff,
      opacity: 0.08,
      transparent: true,
      side: THREE.DoubleSide,
      depthWrite: false,
    })
    const plane = new THREE.Mesh(planeGeometry, planeMaterial)
    plane.rotation.x = -Math.PI / 2
    plane.position.y = level.elevation
    plane.renderOrder = 1
    group.add(plane)

    const lineMaterial = new THREE.LineBasicMaterial({ color: 0x3a86ff, opacity: 0.6, transparent: true, depthTest: true })
    const lineGeometry = new THREE.BufferGeometry().setFromPoints([
      new THREE.Vector3(-100000, level.elevation, -100000),
      new THREE.Vector3(100000, level.elevation, -100000),
      new THREE.Vector3(100000, level.elevation, 100000),
      new THREE.Vector3(-100000, level.elevation, 100000),
      new THREE.Vector3(-100000, level.elevation, -100000),
    ])
    const line = new THREE.Line(lineGeometry, lineMaterial)
    line.renderOrder = 2
    group.add(line)

    const spriteMaterial = new THREE.SpriteMaterial({
      color: 0x3a86ff,
      transparent: true,
      opacity: 0.9,
      depthTest: false,
      depthWrite: false,
    })
    const sprite = new THREE.Sprite(spriteMaterial)
    sprite.position.set(-95000, level.elevation + 500, -95000)
    sprite.scale.set(15000, 1500, 1)
    sprite.renderOrder = 3
    group.add(sprite)

    this.levelGroup.add(group)
    this.levelObjects.set(level.id, group)
  }

  getLevelObject(levelId: string): THREE.Object3D | undefined {
    return this.levelObjects.get(levelId)
  }

  dispose(): void {
    if (this.levelGroup && this.scene) {
      this.levelObjects.forEach((obj) => {
        this.levelGroup?.remove(obj)
        obj.traverse((child) => {
          if (child instanceof THREE.Mesh) {
            child.geometry.dispose()
            const materials = Array.isArray(child.material) ? child.material : [child.material]
            materials.forEach((m) => m.dispose())
          }
          if (child instanceof THREE.Line) {
            child.geometry.dispose()
            const materials = Array.isArray(child.material) ? child.material : [child.material]
            materials.forEach((m) => m.dispose())
          }
          if (child instanceof THREE.Sprite) {
            child.material.dispose()
          }
        })
      })
      this.scene.remove(this.levelGroup)
    }
    this.levels.clear()
    this.levelObjects.clear()
    this.levelGroup = null
    this.scene = null
  }
}
