import * as THREE from 'three'

export class SceneManager {
  private scene: THREE.Scene = new THREE.Scene()

  getScene(): THREE.Scene {
    return this.scene
  }

  setBackground(color: number): void {
    this.scene.background = new THREE.Color(color)
  }

  add(object: THREE.Object3D): void {
    this.scene.add(object)
  }

  remove(object: THREE.Object3D): void {
    this.scene.remove(object)
  }

  clear(): void {
    while (this.scene.children.length > 0) {
      const child = this.scene.children[0]
      this.scene.remove(child)
    }
  }

  dispose(): void {
    this.clear()
  }
}
