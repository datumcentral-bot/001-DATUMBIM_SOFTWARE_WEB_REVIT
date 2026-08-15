export interface SelectionFilter {
  categories: string[]
  types: string[]
  levels: string[]
  worksets: string[]
}

export interface SelectionSet {
  id: string
  name: string
  elements: string[]
  filter: SelectionFilter
  createdAt: Date
}

export interface SelectionEngineState {
  selectedIds: string[]
  selectionSets: SelectionSet[]
  activeSelectionSetId: string | null
  filter: SelectionFilter
  highlightLevel: 'none' | 'low' | 'medium' | 'high'
}

export interface SelectionEventArgs {
  added: string[]
  removed: string[]
  cleared: boolean
}
