import { SelectionEngineState, SelectionEventArgs, SelectionSet, SelectionFilter } from './types/SelectionTypes'

export class SelectionEngine {
  private state: SelectionEngineState = {
    selectedIds: [],
    selectionSets: [],
    activeSelectionSetId: null,
    filter: {
      categories: [],
      types: [],
      levels: [],
      worksets: [],
    },
    highlightLevel: 'none',
  }

  private listeners: Set<(args: SelectionEventArgs) => void> = new Set()

  getState(): SelectionEngineState {
    return this.state
  }

  subscribe(listener: (args: SelectionEventArgs) => void): () => void {
    this.listeners.add(listener)
    return () => this.listeners.delete(listener)
  }

  private notify(args: SelectionEventArgs): void {
    this.listeners.forEach((listener) => listener(args))
  }

  select(id: string, additive: boolean = false): void {
    const args: SelectionEventArgs = { added: [], removed: [], cleared: false }
    if (!additive) {
      const removed = this.state.selectedIds
      this.state.selectedIds = [id]
      args.removed = removed
      args.cleared = true
    } else if (!this.state.selectedIds.includes(id)) {
      this.state.selectedIds.push(id)
      args.added = [id]
    }
    this.notify(args)
  }

  selectMultiple(ids: string[], additive: boolean = false): void {
    const args: SelectionEventArgs = { added: [], removed: [], cleared: false }
    if (!additive) {
      const removed = this.state.selectedIds
      this.state.selectedIds = [...ids]
      args.removed = removed
      args.cleared = true
    } else {
      const newIds = ids.filter((id) => !this.state.selectedIds.includes(id))
      this.state.selectedIds = [...this.state.selectedIds, ...newIds]
      args.added = newIds
    }
    this.notify(args)
  }

  deselect(id: string): void {
    const index = this.state.selectedIds.indexOf(id)
    if (index === -1) return
    this.state.selectedIds.splice(index, 1)
    this.notify({ added: [], removed: [id], cleared: false })
  }

  clearSelection(): void {
    const removed = this.state.selectedIds
    this.state.selectedIds = []
    this.notify({ added: [], removed, cleared: true })
  }

  setFilter(filter: Partial<SelectionFilter>): void {
    this.state.filter = { ...this.state.filter, ...filter }
  }

  createSelectionSet(name: string, ids: string[], filter: SelectionFilter): SelectionSet {
    const set: SelectionSet = {
      id: crypto.randomUUID(),
      name,
      elements: ids,
      filter,
      createdAt: new Date(),
    }
    this.state.selectionSets.push(set)
    return set
  }

  activateSelectionSet(setId: string): void {
    const set = this.state.selectionSets.find((s) => s.id === setId)
    if (!set) return
    this.state.activeSelectionSetId = setId
    this.state.selectedIds = [...set.elements]
  }

  getSelectedCount(): number {
    return this.state.selectedIds.length
  }

  isEmpty(): boolean {
    return this.state.selectedIds.length === 0
  }
}
