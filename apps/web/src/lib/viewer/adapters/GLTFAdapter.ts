import * as THREE from 'three'
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader'
import type { BIMModel, BIMElement, GeometryData, MaterialData, TransformData, ModelLoader } from './FormatAdapters'

export class GLTFGeometryLoader {
  loadGeometry(_geometry: GeometryData): GeometryData {
    return _geometry
  }
}

export class GLTFAdapter implements ModelLoader {
  private loader: GLTFLoader = new GLTFLoader()

  loadModel(data: unknown): BIMModel {
    if (data instanceof Blob || typeof data === 'string') {
      throw new Error('GLTF binary data should be passed as ArrayBuffer or URL string')
    }
    return {
      id: 'gltf-model',
      name: 'GLTF Model',
      elements: [],
      materials: [],
      geometryLoader: new GLTFGeometryLoader(),
    }
  }

  static async loadFromUrl(url: string): Promise<BIMModel> {
    const loader = new GLTFAdapter()
    return loader.loadModel(url)
  }
}
