import * as THREE from 'three'

export class GridManager {
  private scene: THREE.Scene | null = null
  private grid: THREE.GridHelper | null = null
  private axes: THREE.AxesHelper | null = null

  attach(scene: THREE.Scene, size = 200, divisions = 40): void {
    this.scene = scene
    this.grid = new THREE.GridHelper(size, divisions, 0x444444, 0x222222)
    this.axes = new THREE.AxesHelper(20)
    scene.add(this.grid)
    scene.add(this.axes)
  }

  detach(): void {
    if (!this.scene) return
    if (this.grid) this.scene.remove(this.grid)
    if (this.axes) this.scene.remove(this.axes)
    this.grid = null
    this.axes = null
    this.scene = null
  }

  getGrid(): THREE.GridHelper | null {
    return this.grid
  }

  getAxes(): THREE.AxesHelper | null {
    return this.axes
  }
}
