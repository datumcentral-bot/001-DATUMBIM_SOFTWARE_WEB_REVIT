declare module 'three/examples/jsm/controls/OrbitControls' {
  import type { PerspectiveCamera } from 'three'
  export class OrbitControls {
    constructor(camera: PerspectiveCamera, domElement: HTMLElement)
    enableDamping: boolean
    dampingFactor: number
    screenSpacePanning: boolean
    mouseButtons: Record<string, number>
    touches: Record<string, number>
    target: { copy: (v: { x: number; y: number; z: number }) => void }
    update(): void
    dispose(): void
  }
}

declare module 'three/examples/jsm/loaders/GLTFLoader' {
  export class GLTFLoader {
    parse(): void
    load(): void
  }
}
