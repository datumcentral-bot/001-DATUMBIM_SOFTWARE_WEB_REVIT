import { describe, it, expect, beforeEach } from 'vitest'
import { ElementEngine } from '@/lib/design'
import type { ElementDefinition, ElementTypeDefinition } from '@/lib/design'

describe('ElementEngine', () => {
  let engine: ElementEngine

  beforeEach(() => {
    engine = new ElementEngine()
  })

  it('initializes with empty state', () => {
    const state = engine.getState()
    expect(state.size).toBe(0)
  })

  it('registers an element type', () => {
    const type: ElementTypeDefinition = {
      id: 'wall-type',
      name: 'Basic Wall',
      category: 'Walls',
      properties: [],
      baseTransform: {
        position: { x: 0, y: 0, z: 0 },
        rotation: { x: 0, y: 0, z: 0 },
        scale: { x: 1, y: 1, z: 1 },
      },
    }
    engine.registerElementType(type)
    expect(engine.getElementType('wall-type')).toBeDefined()
    expect(engine.getElementType('wall-type')?.name).toBe('Basic Wall')
  })

  it('creates an element from type', () => {
    const type: ElementTypeDefinition = {
      id: 'wall-type',
      name: 'Basic Wall',
      category: 'Walls',
      properties: [],
      baseTransform: {
        position: { x: 0, y: 0, z: 0 },
        rotation: { x: 0, y: 0, z: 0 },
        scale: { x: 1, y: 1, z: 1 },
      },
    }
    engine.registerElementType(type)
    const element = engine.createElement('wall-type')
    expect(element.id).toBeDefined()
    expect(element.typeId).toBe('wall-type')
    expect(element.category).toBe('Walls')
    expect(element.name).toBe('Basic Wall 1')
    expect(engine.getState().size).toBe(1)
  })

  it('throws when creating element with unknown type', () => {
    expect(() => engine.createElement('unknown-type')).toThrow('Element type not found: unknown-type')
  })

  it('gets an element by id', () => {
    const type: ElementTypeDefinition = {
      id: 'wall-type',
      name: 'Basic Wall',
      category: 'Walls',
      properties: [],
      baseTransform: {
        position: { x: 0, y: 0, z: 0 },
        rotation: { x: 0, y: 0, z: 0 },
        scale: { x: 1, y: 1, z: 1 },
      },
    }
    engine.registerElementType(type)
    const element = engine.createElement('wall-type')
    const fetched = engine.getElement(element.id)
    expect(fetched?.id).toBe(element.id)
  })

  it('updates an element', () => {
    const type: ElementTypeDefinition = {
      id: 'wall-type',
      name: 'Basic Wall',
      category: 'Walls',
      properties: [],
      baseTransform: {
        position: { x: 0, y: 0, z: 0 },
        rotation: { x: 0, y: 0, z: 0 },
        scale: { x: 1, y: 1, z: 1 },
      },
    }
    engine.registerElementType(type)
    const element = engine.createElement('wall-type')
    engine.updateElement(element.id, { name: 'Updated Wall' })
    expect(engine.getElement(element.id)?.name).toBe('Updated Wall')
  })

  it('throws when updating unknown element', () => {
    expect(() => engine.updateElement('unknown', { name: 'Test' })).toThrow('Element not found: unknown')
  })

  it('deletes an element', () => {
    const type: ElementTypeDefinition = {
      id: 'wall-type',
      name: 'Basic Wall',
      category: 'Walls',
      properties: [],
      baseTransform: {
        position: { x: 0, y: 0, z: 0 },
        rotation: { x: 0, y: 0, z: 0 },
        scale: { x: 1, y: 1, z: 1 },
      },
    }
    engine.registerElementType(type)
    const element = engine.createElement('wall-type')
    engine.deleteElement(element.id)
    expect(engine.getState().size).toBe(0)
  })

  it('filters elements by category', () => {
    const wallType: ElementTypeDefinition = {
      id: 'wall-type',
      name: 'Basic Wall',
      category: 'Walls',
      properties: [],
      baseTransform: { position: { x: 0, y: 0, z: 0 }, rotation: { x: 0, y: 0, z: 0 }, scale: { x: 1, y: 1, z: 1 } },
    }
    const doorType: ElementTypeDefinition = {
      id: 'door-type',
      name: 'Single-Flush',
      category: 'Doors',
      properties: [],
      baseTransform: { position: { x: 0, y: 0, z: 0 }, rotation: { x: 0, y: 0, z: 0 }, scale: { x: 1, y: 1, z: 1 } },
    }
    engine.registerElementType(wallType)
    engine.registerElementType(doorType)
    engine.createElement('wall-type')
    engine.createElement('door-type')
    const walls = engine.getElementsByCategory('Walls')
    expect(walls).toHaveLength(1)
  })

  it('filters elements by type', () => {
    const wallType: ElementTypeDefinition = {
      id: 'wall-type',
      name: 'Basic Wall',
      category: 'Walls',
      properties: [],
      baseTransform: { position: { x: 0, y: 0, z: 0 }, rotation: { x: 0, y: 0, z: 0 }, scale: { x: 1, y: 1, z: 1 } },
    }
    engine.registerElementType(wallType)
    engine.createElement('wall-type')
    engine.createElement('wall-type')
    const walls = engine.getElementsByType('wall-type')
    expect(walls).toHaveLength(2)
  })

  it('sets selection state', () => {
    const type: ElementTypeDefinition = {
      id: 'wall-type',
      name: 'Basic Wall',
      category: 'Walls',
      properties: [],
      baseTransform: { position: { x: 0, y: 0, z: 0 }, rotation: { x: 0, y: 0, z: 0 }, scale: { x: 1, y: 1, z: 1 } },
    }
    engine.registerElementType(type)
    const element = engine.createElement('wall-type')
    engine.setSelectionState(element.id, { selected: true, highlightLevel: 'high' })
    expect(engine.getElement(element.id)?.selectionState.selected).toBe(true)
    expect(engine.getElement(element.id)?.selectionState.highlightLevel).toBe('high')
  })

  it('sets visibility', () => {
    const type: ElementTypeDefinition = {
      id: 'wall-type',
      name: 'Basic Wall',
      category: 'Walls',
      properties: [],
      baseTransform: { position: { x: 0, y: 0, z: 0 }, rotation: { x: 0, y: 0, z: 0 }, scale: { x: 1, y: 1, z: 1 } },
    }
    engine.registerElementType(type)
    const element = engine.createElement('wall-type')
    engine.setVisibility(element.id, false)
    expect(engine.getElement(element.id)?.visibility).toBe(false)
  })
})
