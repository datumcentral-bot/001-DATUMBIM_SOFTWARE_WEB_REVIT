/// <reference types="vitest/globals" />

import { describe, it, expect, beforeEach } from 'vitest'
import { ViewEngine } from '@/lib/design'
import type { ViewDefinition, CameraState } from '@/lib/design'

describe('ViewEngine', () => {
  let engine: ViewEngine

  beforeEach(() => {
    engine = new ViewEngine()
  })

  it('initializes with empty state', () => {
    const state = engine.getState()
    expect(state.views).toEqual([])
    expect(state.activeViewId).toBeNull()
    expect(state.cameraState).toBeNull()
  })

  it('registers a view', () => {
    const view: ViewDefinition = {
      id: 'view-1',
      name: 'Test View',
      type: '3d',
      discipline: 'generic',
      visibilityState: true,
      activeState: false,
    }
    engine.registerView(view)
    expect(engine.getState().views).toHaveLength(1)
    expect(engine.getState().views[0].id).toBe('view-1')
  })

  it('updates an existing view', () => {
    const view: ViewDefinition = {
      id: 'view-1',
      name: 'Test View',
      type: '3d',
      discipline: 'generic',
      visibilityState: true,
      activeState: false,
    }
    engine.registerView(view)
    engine.registerView({ ...view, name: 'Updated View' })
    expect(engine.getState().views).toHaveLength(1)
    expect(engine.getState().views[0].name).toBe('Updated View')
  })

  it('unregisters a view', () => {
    const view: ViewDefinition = {
      id: 'view-1',
      name: 'Test View',
      type: '3d',
      discipline: 'generic',
      visibilityState: true,
      activeState: false,
    }
    engine.registerView(view)
    engine.unregisterView('view-1')
    expect(engine.getState().views).toHaveLength(0)
  })

  it('sets active view', () => {
    const view: ViewDefinition = {
      id: 'view-1',
      name: 'Test View',
      type: '3d',
      discipline: 'generic',
      visibilityState: true,
      activeState: false,
      cameraState: { position: { x: 1, y: 2, z: 3 }, target: { x: 0, y: 0, z: 0 }, up: { x: 0, y: 1, z: 0 } },
    }
    engine.registerView(view)
    engine.setActiveView('view-1')
    expect(engine.getState().activeViewId).toBe('view-1')
    expect(engine.getState().cameraState).toEqual(view.cameraState)
  })

  it('auto-creates view when setting non-existent view as active', () => {
    engine.setActiveView('nonexistent')
    expect(engine.getState().activeViewId).toBe('nonexistent')
    expect(engine.getState().views).toHaveLength(1)
    expect(engine.getState().views[0].id).toBe('nonexistent')
  })

  it('returns null for getActiveView when no active view', () => {
    expect(engine.getActiveView()).toBeNull()
  })

  it('returns active view', () => {
    const view: ViewDefinition = {
      id: 'view-1',
      name: 'Test View',
      type: '3d',
      discipline: 'generic',
      visibilityState: true,
      activeState: false,
    }
    engine.registerView(view)
    engine.setActiveView('view-1')
    expect(engine.getActiveView()?.id).toBe('view-1')
  })

  it('updates camera state', () => {
    engine.updateCameraState({ position: { x: 10, y: 20, z: 30 } })
    const state = engine.getState()
    expect(state.cameraState?.position).toEqual({ x: 10, y: 20, z: 30 })
    expect(state.cameraState?.target).toEqual({ x: 0, y: 0, z: 0 })
    expect(state.cameraState?.up).toEqual({ x: 0, y: 1, z: 0 })
  })

  it('filters views by type', () => {
    engine.registerView({ id: 'v1', name: '3D', type: '3d', discipline: 'generic', visibilityState: true, activeState: false })
    engine.registerView({ id: 'v2', name: 'Plan', type: 'floor-plan', discipline: 'architecture', visibilityState: true, activeState: false })
    engine.registerView({ id: 'v3', name: '3D 2', type: '3d', discipline: 'generic', visibilityState: true, activeState: false })
    const views3d = engine.getViewsByType('3d')
    expect(views3d).toHaveLength(2)
  })

  it('filters views by discipline', () => {
    engine.registerView({ id: 'v1', name: '3D', type: '3d', discipline: 'generic', visibilityState: true, activeState: false })
    engine.registerView({ id: 'v2', name: 'Plan', type: 'floor-plan', discipline: 'architecture', visibilityState: true, activeState: false })
    const archViews = engine.getViewsByDiscipline('architecture')
    expect(archViews).toHaveLength(1)
  })

  it('subscribes to state changes', () => {
    const listener = vi.fn()
    engine.subscribe(listener)
    engine.registerView({ id: 'v1', name: 'Test', type: '3d', discipline: 'generic', visibilityState: true, activeState: false })
    expect(listener).toHaveBeenCalled()
  })
})
