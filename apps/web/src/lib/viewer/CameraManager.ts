import * as THREE from 'three'
import type { CameraState } from '@/lib/design/types/ViewTypes'

export class CameraManager {
  private perspective: THREE.PerspectiveCamera | null = null
  private orthographic: THREE.OrthographicCamera | null = null
  private active: THREE.PerspectiveCamera | THREE.OrthographicCamera | null = null
  private mode: 'perspective' | 'orthographic' = 'perspective'

  initialize(width: number, height: number): void {
    const aspect = width / height
    this.perspective = new THREE.PerspectiveCamera(50, aspect, 1, 100000)
    this.perspective.position.set(20000, 15000, 20000)
    this.perspective.up.set(0, 1, 0)
    this.perspective.lookAt(0, 0, 0)

    const frustumSize = 200
    this.orthographic = new THREE.OrthographicCamera(
      -frustumSize * aspect,
      frustumSize * aspect,
      frustumSize,
      -frustumSize,
      0.1,
      100000
    )
    this.orthographic.position.set(20000, 15000, 20000)
    this.orthographic.up.set(0, 1, 0)
    this.orthographic.lookAt(0, 0, 0)

    this.active = this.perspective
  }

  getActive(): THREE.PerspectiveCamera | THREE.OrthographicCamera | null {
    return this.active
  }

  getMode(): 'perspective' | 'orthographic' {
    return this.mode
  }

  setMode(mode: 'perspective' | 'orthographic'): void {
    if (this.mode === mode) return
    this.mode = mode
    if (mode === 'perspective') {
      this.active = this.perspective
    } else {
      this.active = this.orthographic
    }
  }

  applyCameraState(state: CameraState): void {
    const target = new THREE.Vector3(state.target.x, state.target.y, state.target.z)
    const position = new THREE.Vector3(state.position.x, state.position.y, state.position.z)
    const up = new THREE.Vector3(state.up.x, state.up.y, state.up.z)
    if (this.perspective) {
      this.perspective.position.copy(position)
      this.perspective.up.copy(up)
      this.perspective.lookAt(target)
    }
    if (this.orthographic) {
      this.orthographic.position.copy(position)
      this.orthographic.up.copy(up)
      this.orthographic.lookAt(target)
    }
  }

  getCameraState(): CameraState | null {
    if (!this.active) return null
    return {
      position: { x: this.active.position.x, y: this.active.position.y, z: this.active.position.z },
      target: { x: 0, y: 0, z: 0 },
      up: { x: this.active.up.x, y: this.active.up.y, z: this.active.up.z },
    }
  }

  resize(width: number, height: number): void {
    if (this.perspective) {
      this.perspective.aspect = width / height
      this.perspective.updateProjectionMatrix()
    }
    const aspect = width / height
    const frustumSize = 200
    if (this.orthographic) {
      this.orthographic.left = -frustumSize * aspect
      this.orthographic.right = frustumSize * aspect
      this.orthographic.top = frustumSize
      this.orthographic.bottom = -frustumSize
      this.orthographic.updateProjectionMatrix()
    }
  }

  dispose(): void {
    this.perspective = null
    this.orthographic = null
    this.active = null
  }
}
