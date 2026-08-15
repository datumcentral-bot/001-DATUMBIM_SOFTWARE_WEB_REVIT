import * as THREE from 'three'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls'
import type { ViewerContext } from './types/ViewerTypes'

export class ControlsManager {
  private controls: OrbitControls | null = null
  private context: ViewerContext | null = null

  initialize(context: ViewerContext): OrbitControls {
    this.context = context
    const camera = context.camera as unknown as THREE.PerspectiveCamera
    if (!(camera instanceof THREE.PerspectiveCamera)) {
      throw new Error('ControlsManager requires a PerspectiveCamera')
    }
    this.controls = new OrbitControls(camera, context.container!)
    this.controls.enableDamping = true
    this.controls.dampingFactor = 0.1
    this.controls.screenSpacePanning = true
    this.controls.mouseButtons = {
      LEFT: null as unknown as THREE.MOUSE,
      MIDDLE: THREE.MOUSE.PAN,
      RIGHT: THREE.MOUSE.ROTATE,
    }
    this.controls.touches = {
      ONE: THREE.TOUCH.ROTATE,
      TWO: THREE.TOUCH.DOLLY_PAN,
    }
    return this.controls
  }

  getControls(): OrbitControls | null {
    return this.controls
  }

  update(): void {
    this.controls?.update()
  }

  dispose(): void {
    if (this.controls) {
      this.controls.dispose()
      this.controls = null
    }
    this.context = null
  }
}
