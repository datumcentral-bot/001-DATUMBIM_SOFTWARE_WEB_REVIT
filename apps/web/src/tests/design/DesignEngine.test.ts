/// <reference types="vitest/globals" />

import { describe, it, expect, beforeEach } from 'vitest'
import { DesignEngine } from '@/lib/design'

describe('DesignEngine', () => {
  let engine: DesignEngine

  beforeEach(() => {
    engine = new DesignEngine()
  })

  it('initializes with default state', () => {
    const state = engine.getState()
    expect(state.initialized).toBe(false)
    expect(state.activeViewId).toBeNull()
    expect(state.selectedElementIds).toEqual([])
    expect(state.renderContext).toBeNull()
  })

  it('initializes the engine', () => {
    engine.initialize()
    expect(engine.isInitialized()).toBe(true)
    expect(engine.getState().initialized).toBe(true)
  })

  it('does not re-initialize if already initialized', () => {
    engine.initialize()
    engine.initialize()
    expect(engine.isInitialized()).toBe(true)
  })

  it('disposes the engine', () => {
    engine.initialize()
    engine.dispose()
    expect(engine.isInitialized()).toBe(false)
    expect(engine.getState().initialized).toBe(false)
  })

  it('subscribes and notifies listeners', () => {
    const listener = vi.fn()
    engine.subscribe(listener)
    engine.initialize()
    expect(listener).toHaveBeenCalledTimes(1)
  })

  it('unsubscribes listeners', () => {
    const listener = vi.fn()
    const unsubscribe = engine.subscribe(listener)
    unsubscribe()
    engine.initialize()
    expect(listener).not.toHaveBeenCalled()
  })

  it('exposes sub-engines', () => {
    expect(engine.viewEngine).toBeInstanceOf(engine.viewEngine.constructor)
    expect(engine.elementEngine).toBeInstanceOf(engine.elementEngine.constructor)
    expect(engine.selectionEngine).toBeInstanceOf(engine.selectionEngine.constructor)
    expect(engine.transformEngine).toBeInstanceOf(engine.transformEngine.constructor)
    expect(engine.renderEngine).toBeInstanceOf(engine.renderEngine.constructor)
  })
})
