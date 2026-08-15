import * as THREE from 'three'
import type { ViewerBIMElement, ViewerModelReference, ViewerMaterial } from './types/ViewerTypes'
import type { BIMModel, BIMElement, GeometryData, MaterialData, ModelLoader, GeometryLoader } from './adapters/FormatAdapters'

export class ModelManager {
  private model: ViewerModelReference | null = null
  private root: THREE.Group | null = null
  private elements: Map<string, ViewerBIMElement> = new Map()
  private materials: Map<string, THREE.Material> = new Map()
  private viewerMaterials: Map<string, ViewerMaterial> = new Map()
  private scene: THREE.Scene | null = null
  private listeners: Set<(model: ViewerModelReference | null) => void> = new Set()

  initialize(scene: THREE.Scene): void {
    this.scene = scene
    this.root = new THREE.Group()
    this.root.name = 'BIM-Model-Root'
    scene.add(this.root)
  }

  getRoot(): THREE.Group | null {
    return this.root
  }

  getElements(): ViewerBIMElement[] {
    return Array.from(this.elements.values())
  }

  getElement(id: string): ViewerBIMElement | undefined {
    return this.elements.get(id)
  }

  getMaterial(id: string): THREE.Material | undefined {
    return this.materials.get(id)
  }

  getViewerMaterial(id: string): ViewerMaterial | undefined {
    return this.viewerMaterials.get(id)
  }

  getModel(): ViewerModelReference | null {
    return this.model
  }

  subscribe(listener: (model: ViewerModelReference | null) => void): () => void {
    this.listeners.add(listener)
    return () => this.listeners.delete(listener)
  }

  private notify(model: ViewerModelReference | null): void {
    this.listeners.forEach((listener) => listener(model))
  }

  loadModel(adapter: ModelLoader, data: unknown): ViewerModelReference {
    if (!this.root || !this.scene) {
      throw new Error('ModelManager not initialized')
    }
    const model = adapter.loadModel(data)
    this.setModel(model)
    return this.model!
  }

  setModel(model: BIMModel): void {
    if (!this.root || !this.scene) {
      throw new Error('ModelManager not initialized')
    }
    while (this.root.children.length > 0) {
      const child = this.root.children[0]
      this.root.remove(child)
    }
    this.elements.clear()
    this.materials.clear()
    this.viewerMaterials.clear()

    const ref: ViewerModelReference = {
      id: model.id,
      name: model.name,
      loaded: true,
      root: this.root,
    }
    this.model = ref

    const loader = model.geometryLoader
    for (const element of model.elements) {
      this.addElement(element, loader)
    }

    this.notify(ref)
  }

  addElement(element: BIMElement, loader: GeometryLoader): void {
    if (!this.root) return
    const material = this.ensureMaterial(element.material)
    const geometryData = loader.loadGeometry(element.geometry)
    let geometry: THREE.BufferGeometry
    switch (geometryData.type) {
      case 'box':
        geometry = new THREE.BoxGeometry(geometryData.width, geometryData.height, geometryData.depth)
        break
      case 'plane':
        geometry = new THREE.PlaneGeometry(geometryData.width, geometryData.height)
        break
      case 'cylinder':
        geometry = new THREE.CylinderGeometry(geometryData.radiusTop, geometryData.radiusBottom, geometryData.height, 32)
        break
      case 'sphere':
        geometry = new THREE.SphereGeometry(geometryData.radius, 32, 16)
        break
      case 'line':
        geometry = new THREE.BufferGeometry().setFromPoints((geometryData.points ?? []).map((p) => new THREE.Vector3(p.x, p.y, p.z)))
        break
      default:
        geometry = new THREE.BoxGeometry(1, 1, 1)
    }

    const mesh = new THREE.Mesh(geometry, material)
    mesh.position.set(element.transform.position.x, element.transform.position.y, element.transform.position.z)
    mesh.rotation.set(element.transform.rotation.x, element.transform.rotation.y, element.transform.rotation.z)
    mesh.scale.set(element.transform.scale.x, element.transform.scale.y, element.transform.scale.z)
    mesh.visible = element.visible

    const viewerElement: ViewerBIMElement = {
      id: element.id,
      category: element.category,
      family: element.family,
      type: element.type,
      level: element.level,
      name: element.name,
      visible: element.visible,
      materialId: element.material.id,
      source: element.source,
      modelId: element.modelId,
      metadata: element.metadata,
      threeObject: mesh,
    }
    this.elements.set(element.id, viewerElement)
    this.root.add(mesh)
  }

  updateVisibility(elementId: string, visible: boolean): void {
    const element = this.elements.get(elementId)
    if (element && element.threeObject instanceof THREE.Mesh) {
      element.visible = visible
      element.threeObject.visible = visible
    }
  }

  private ensureMaterial(materialData: MaterialData): THREE.Material {
    if (this.materials.has(materialData.id)) {
      return this.materials.get(materialData.id)!
    }
    const material = new THREE.MeshStandardMaterial({
      color: materialData.color,
      opacity: materialData.opacity,
      roughness: materialData.roughness,
      metalness: materialData.metalness,
      transparent: materialData.transparent,
    })
    this.materials.set(materialData.id, material)
    this.viewerMaterials.set(materialData.id, {
      id: materialData.id,
      name: materialData.name,
      color: materialData.color,
      opacity: materialData.opacity,
      roughness: materialData.roughness,
      metalness: materialData.metalness,
      transparent: materialData.transparent,
    })
    return material
  }

  getRecursiveObjects(): THREE.Object3D[] {
    if (!this.root) return []
    const objects: THREE.Object3D[] = []
    this.root.traverse((child) => {
      if (child instanceof THREE.Mesh) {
        objects.push(child)
      }
    })
    return objects
  }

  dispose(): void {
    if (this.root && this.scene) {
      this.scene.remove(this.root)
    }
    this.elements.forEach((element) => {
      const obj = element.threeObject as THREE.Object3D
      if (obj instanceof THREE.Mesh) {
        obj.geometry.dispose()
        const material = Array.isArray(obj.material) ? obj.material : [obj.material]
        material.forEach((m) => m.dispose())
      }
    })
    this.materials.forEach((m) => m.dispose())
    this.elements.clear()
    this.materials.clear()
    this.viewerMaterials.clear()
    this.root = null
    this.scene = null
    this.model = null
    this.notify(null)
  }
}
