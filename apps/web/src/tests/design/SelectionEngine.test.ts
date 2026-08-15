/// <reference types="vitest/globals" />

import { describe, it, expect, beforeEach } from 'vitest'
import { SelectionEngine } from '@/lib/design'

describe('SelectionEngine', () => {
  let engine: SelectionEngine

  beforeEach(() => {
    engine = new SelectionEngine()
  })

  it('initializes with empty selection', () => {
    const state = engine.getState()
    expect(state.selectedIds).toEqual([])
    expect(state.selectionSets).toEqual([])
    expect(state.activeSelectionSetId).toBeNull()
    expect(state.highlightLevel).toBe('none')
  })

  it('selects an element', () => {
    engine.select('element-1')
    expect(engine.getState().selectedIds).toEqual(['element-1'])
    expect(engine.isEmpty()).toBe(false)
    expect(engine.getSelectedCount()).toBe(1)
  })

  it('clears previous selection when selecting additively false', () => {
    engine.select('element-1')
    engine.select('element-2', false)
    expect(engine.getState().selectedIds).toEqual(['element-2'])
  })

  it('adds to selection when additive is true', () => {
    engine.select('element-1')
    engine.select('element-2', true)
    expect(engine.getState().selectedIds).toEqual(['element-1', 'element-2'])
    expect(engine.getSelectedCount()).toBe(2)
  })

  it('deselects an element', () => {
    engine.select('element-1')
    engine.select('element-2', true)
    engine.deselect('element-1')
    expect(engine.getState().selectedIds).toEqual(['element-2'])
  })

  it('clears selection', () => {
    engine.select('element-1')
    engine.select('element-2', true)
    engine.clearSelection()
    expect(engine.getState().selectedIds).toEqual([])
    expect(engine.isEmpty()).toBe(true)
  })

  it('selects multiple elements', () => {
    engine.selectMultiple(['element-1', 'element-2', 'element-3'])
    expect(engine.getState().selectedIds).toHaveLength(3)
  })

  it('selects multiple additively', () => {
    engine.select('element-1')
    engine.selectMultiple(['element-2', 'element-3'], true)
    expect(engine.getState().selectedIds).toHaveLength(3)
  })

  it('sets filter', () => {
    engine.setFilter({ categories: ['Walls', 'Doors'], types: ['wall-type'] })
    const state = engine.getState()
    expect(state.filter.categories).toEqual(['Walls', 'Doors'])
    expect(state.filter.types).toEqual(['wall-type'])
  })

  it('creates a selection set', () => {
    engine.selectMultiple(['element-1', 'element-2'])
    const selectionSet = engine.createSelectionSet('My Set', ['element-1', 'element-2'], {
      categories: [],
      types: [],
      levels: [],
      worksets: [],
    })
    expect(selectionSet.id).toBeDefined()
    expect(selectionSet.name).toBe('My Set')
    expect(engine.getState().selectionSets).toHaveLength(1)
  })

  it('activates a selection set', () => {
    engine.selectMultiple(['element-1', 'element-2'])
    const selectionSet = engine.createSelectionSet('My Set', ['element-1', 'element-2'], {
      categories: [],
      types: [],
      levels: [],
      worksets: [],
    })
    engine.activateSelectionSet(selectionSet.id)
    expect(engine.getState().activeSelectionSetId).toBe(selectionSet.id)
    expect(engine.getState().selectedIds).toEqual(['element-1', 'element-2'])
  })

  it('subscribes to selection events', () => {
    const listener = vi.fn()
    engine.subscribe(listener)
    engine.select('element-1')
    expect(listener).toHaveBeenCalled()
  })

  it('unsubscribes from selection events', () => {
    const listener = vi.fn()
    const unsubscribe = engine.subscribe(listener)
    unsubscribe()
    engine.select('element-1')
    expect(listener).not.toHaveBeenCalled()
  })
})
