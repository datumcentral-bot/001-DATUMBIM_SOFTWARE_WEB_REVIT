import * as THREE from 'three'

export class LightingManager {
  private scene: THREE.Scene | null = null
  private ambient: THREE.AmbientLight | null = null
  private directional: THREE.DirectionalLight | null = null
  private hemisphere: THREE.HemisphereLight | null = null

  attach(scene: THREE.Scene): void {
    this.scene = scene
    this.ambient = new THREE.AmbientLight(0xffffff, 0.6)
    this.directional = new THREE.DirectionalLight(0xffffff, 0.8)
    this.directional.position.set(50, 100, 50)
    this.hemisphere = new THREE.HemisphereLight(0xffffff, 0x444444, 0.3)
    scene.add(this.ambient)
    scene.add(this.directional)
    scene.add(this.hemisphere)
  }

  detach(): void {
    if (!this.scene) return
    if (this.ambient) this.scene.remove(this.ambient)
    if (this.directional) this.scene.remove(this.directional)
    if (this.hemisphere) this.scene.remove(this.hemisphere)
    this.ambient = null
    this.directional = null
    this.hemisphere = null
    this.scene = null
  }

  getLights(): { ambient: THREE.AmbientLight | null; directional: THREE.DirectionalLight | null; hemisphere: THREE.HemisphereLight | null } {
    return { ambient: this.ambient, directional: this.directional, hemisphere: this.hemisphere }
  }
}
