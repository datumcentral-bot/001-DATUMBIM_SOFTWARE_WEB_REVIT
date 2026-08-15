import * as THREE from 'three'
import type { BIMModel, BIMElement, GeometryData, MaterialData, TransformData } from '../adapters/FormatAdapters'

const DEFAULT_MATERIALS: MaterialData[] = [
  { id: 'mat-concrete', name: 'Concrete', color: 0x999999, opacity: 1, roughness: 0.8, metalness: 0.1, transparent: false },
  { id: 'mat-steel', name: 'Steel', color: 0x666666, opacity: 1, roughness: 0.4, metalness: 0.9, transparent: false },
  { id: 'mat-glass', name: 'Glass', color: 0x88ccff, opacity: 0.4, roughness: 0.1, metalness: 0.1, transparent: true },
  { id: 'mat-wood', name: 'Wood', color: 0x8b5a2b, opacity: 1, roughness: 0.7, metalness: 0.0, transparent: false },
  { id: 'mat-wall', name: 'Wall Finish', color: 0xcccccc, opacity: 1, roughness: 0.6, metalness: 0.05, transparent: false },
  { id: 'mat-floor', name: 'Floor', color: 0x777777, opacity: 1, roughness: 0.5, metalness: 0.1, transparent: false },
  { id: 'mat-roof', name: 'Roof', color: 0x555555, opacity: 1, roughness: 0.6, metalness: 0.1, transparent: false },
  { id: 'mat-duct', name: 'Duct', color: 0xcc3333, opacity: 1, roughness: 0.5, metalness: 0.3, transparent: false },
  { id: 'mat-pipe', name: 'Pipe', color: 0x3399cc, opacity: 1, roughness: 0.4, metalness: 0.5, transparent: false },
]

function material(name: string): MaterialData {
  const found = DEFAULT_MATERIALS.find((m) => m.name === name)
  return found ?? DEFAULT_MATERIALS[0]
}

function box(w: number, h: number, d: number): GeometryData {
  return { type: 'box', width: w, height: h, depth: d }
}

function plane(w: number, h: number): GeometryData {
  return { type: 'plane', width: w, height: h }
}

function cylinder(rt = 0.5, rb = 0.5, h = 1): GeometryData {
  return { type: 'cylinder', radiusTop: rt, radiusBottom: rb, height: h }
}

function makeTransform(x = 0, y = 0, z = 0, rx = 0, ry = 0, rz = 0, sx = 1, sy = 1, sz = 1): TransformData {
  return { position: { x, y, z }, rotation: { x: rx, y: ry, z: rz }, scale: { x: sx, y: sy, z: sz } }
}

function elem(id: string, category: string, name: string, level: string, geometry: GeometryData, matName: string, transform: TransformData): BIMElement {
  const mat = material(matName)
  return {
    id,
    category,
    family: category,
    type: name,
    level,
    name,
    visible: true,
    geometry,
    transform,
    material: mat,
    source: 'demo-model',
    modelId: 'demo-model',
    metadata: {},
  }
}

export class DemoModelBuilder {
  static build(): BIMModel {
    const elements: BIMElement[] = []
    const levels = ['Level 0', 'Level 1', 'Level 2']
    const levelHeight = 3000

    for (const levelName of levels) {
      const y = levels.indexOf(levelName) * levelHeight
      const levelId = levelName.toLowerCase().replace(/\s+/g, '-')

      elements.push(elem(`${levelId}-floor`, 'Floor', 'Floor Slab', levelName, plane(20000, 20000), 'mat-floor', makeTransform(0, y, 0, -Math.PI / 2, 0, 0)))

      const wallLength = 6000
      const wallThickness = 300
      const wallHeight = 3000
      const wallPositions = [
        { x: 0, z: 0, ry: 0 },
        { x: wallLength / 2, z: -wallLength / 2, ry: Math.PI / 2 },
        { x: 0, z: -wallLength, ry: 0 },
        { x: -wallLength / 2, z: -wallLength / 2, ry: Math.PI / 2 },
      ]
      wallPositions.forEach((pos, i) => {
        elements.push(elem(`${levelId}-wall-${i + 1}`, 'Wall', 'Basic Wall', levelName, box(wallThickness, wallHeight, wallLength / 2), 'mat-wall', makeTransform(pos.x, y + wallHeight / 2, pos.z, 0, pos.ry, 0)))
      })

      const columnPositions = [
        { x: -wallLength / 2, z: -wallLength / 2 },
        { x: wallLength / 2, z: -wallLength / 2 },
        { x: -wallLength / 2, z: wallLength / 2 },
        { x: wallLength / 2, z: wallLength / 2 },
      ]
      columnPositions.forEach((pos, i) => {
        elements.push(elem(`${levelId}-col-${i + 1}`, 'Column', 'Concrete Column', levelName, cylinder(150, 150, wallHeight), 'mat-concrete', makeTransform(pos.x, y + wallHeight / 2, pos.z)))
      })

      const beamLength = wallLength / 2
      const beamPositions = [
        { x: 0, z: -wallLength / 2 },
        { x: 0, z: wallLength / 2 },
      ]
      beamPositions.forEach((pos, i) => {
        elements.push(elem(`${levelId}-beam-${i + 1}`, 'Beam', 'Steel Beam', levelName, box(400, 400, beamLength), 'mat-steel', makeTransform(pos.x, y + wallHeight - 200, pos.z)))
      })

      const doorPositions = [
        { x: -wallLength / 4, z: 0 },
        { x: wallLength / 4, z: -wallLength },
      ]
      doorPositions.forEach((pos, i) => {
        elements.push(elem(`${levelId}-door-${i + 1}`, 'Door', 'Single-Flush', levelName, box(100, 2100, 50), 'mat-wood', makeTransform(pos.x, y + 1050, pos.z)))
      })

      const windowPositions = [
        { x: 0, z: -wallLength / 2 },
        { x: wallLength / 2, z: -wallLength / 2 },
      ]
      windowPositions.forEach((pos, i) => {
        elements.push(elem(`${levelId}-window-${i + 1}`, 'Window', 'Fixed', levelName, box(1200, 1500, 50), 'mat-glass', makeTransform(pos.x, y + 1500, pos.z)))
      })

      const ductPositions = [
        { x: 2000, z: -2000 },
        { x: -2000, z: -2000 },
      ]
      ductPositions.forEach((pos, i) => {
        elements.push(elem(`${levelId}-duct-${i + 1}`, 'Duct', 'Rectangular Duct', levelName, box(400, 400, 4000), 'mat-duct', makeTransform(pos.x, y + 2500, pos.z)))
      })

      const pipePositions = [
        { x: 1000, z: 1000 },
        { x: -1000, z: 1000 },
      ]
      pipePositions.forEach((pos, i) => {
        elements.push(elem(`${levelId}-pipe-${i + 1}`, 'Pipe', 'Copper Pipe', levelName, cylinder(100, 100, 4000), 'mat-pipe', makeTransform(pos.x, y + 2600, pos.z)))
      })
    }

    elements.push(elem('roof-1', 'Roof', 'Roof Slab', 'Roof', plane(22000, 22000), 'mat-roof', makeTransform(0, 3 * levelHeight + 200, 0, -Math.PI / 2, 0, 0)))

    return {
      id: 'demo-model',
      name: 'Demo BIM Model',
      elements,
      materials: DEFAULT_MATERIALS,
      geometryLoader: {
        loadGeometry: (g: GeometryData) => g,
      },
    }
  }
}
