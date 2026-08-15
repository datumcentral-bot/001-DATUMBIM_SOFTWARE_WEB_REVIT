import { ElementDefinition, ElementTypeDefinition, SelectionState, ElementMetadata } from './types/ElementTypes'

export class ElementEngine {
  private elements: Map<string, ElementDefinition> = new Map()
  private elementTypes: Map<string, ElementTypeDefinition> = new Map()
  private listeners: Set<() => void> = new Set()

  getState(): Map<string, ElementDefinition> {
    return this.elements
  }

  subscribe(listener: () => void): () => void {
    this.listeners.add(listener)
    return () => this.listeners.delete(listener)
  }

  private notify(): void {
    this.listeners.forEach((listener) => listener())
  }

  registerElementType(type: ElementTypeDefinition): void {
    this.elementTypes.set(type.id, type)
  }

  getElementType(typeId: string): ElementTypeDefinition | undefined {
    return this.elementTypes.get(typeId)
  }

  createElement(typeId: string, overrides: Partial<ElementDefinition> = {}): ElementDefinition {
    const type = this.elementTypes.get(typeId)
    if (!type) {
      throw new Error(`Element type not found: ${typeId}`)
    }

    const element: ElementDefinition = {
      id: crypto.randomUUID(),
      typeId,
      category: type.category,
      name: `${type.name} ${this.elements.size + 1}`,
      properties: {},
      transform: { ...type.baseTransform },
      visibility: true,
      selectionState: { selected: false, highlightLevel: 'none', isolationState: 'none' },
      metadata: {
        createdAt: new Date(),
        source: 'design-engine',
      },
      ...overrides,
    }

    this.elements.set(element.id, element)
    this.notify()
    return element
  }

  getElement(id: string): ElementDefinition | undefined {
    return this.elements.get(id)
  }

  updateElement(id: string, updates: Partial<ElementDefinition>): void {
    const existing = this.elements.get(id)
    if (!existing) {
      throw new Error(`Element not found: ${id}`)
    }
    this.elements.set(id, { ...existing, ...updates, metadata: { ...existing.metadata, modifiedAt: new Date() } })
    this.notify()
  }

  deleteElement(id: string): void {
    this.elements.delete(id)
    this.notify()
  }

  getElementsByCategory(category: string): ElementDefinition[] {
    return Array.from(this.elements.values()).filter((e) => e.category === category)
  }

  getElementsByType(typeId: string): ElementDefinition[] {
    return Array.from(this.elements.values()).filter((e) => e.typeId === typeId)
  }

  setSelectionState(id: string, state: Partial<SelectionState>): void {
    const element = this.elements.get(id)
    if (!element) return
    element.selectionState = { ...element.selectionState, ...state }
    this.notify()
  }

  setVisibility(id: string, visible: boolean): void {
    const element = this.elements.get(id)
    if (!element) return
    element.visibility = visible
    this.notify()
  }
}
