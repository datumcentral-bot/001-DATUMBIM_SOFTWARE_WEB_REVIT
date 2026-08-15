/// <reference types="vitest/globals" />

import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest'
import * as THREE from 'three'
import { SceneManager } from '@/lib/viewer'
import { CameraManager } from '@/lib/viewer'
import { RendererManager } from '@/lib/viewer'
import { ControlsManager } from '@/lib/viewer'
import { SelectionManager } from '@/lib/viewer'
import { ModelManager } from '@/lib/viewer'
import { GridManager } from '@/lib/viewer'
import { LightingManager } from '@/lib/viewer'
import { ViewerEngine } from '@/lib/viewer'
import { DemoModelBuilder } from '@/lib/viewer'
import type { ViewerBIMElement } from '@/lib/viewer'

describe('SceneManager', () => {
  it('creates a scene', () => {
    const manager = new SceneManager()
    const scene = manager.getScene()
    expect(scene).toBeDefined()
    expect(scene.children.length).toBe(0)
  })

  it('adds and removes objects', () => {
    const manager = new SceneManager()
    const scene = manager.getScene()
    const obj = new THREE.Object3D()
    manager.add(obj)
    expect(scene.children.length).toBe(1)
    manager.remove(obj)
    expect(scene.children.length).toBe(0)
  })

  it('clears the scene', () => {
    const manager = new SceneManager()
    const scene = manager.getScene()
    manager.add(new THREE.Object3D())
    manager.add(new THREE.Object3D())
    manager.clear()
    expect(scene.children.length).toBe(0)
  })
})

describe('CameraManager', () => {
  it('initializes perspective and orthographic cameras', () => {
    const manager = new CameraManager()
    manager.initialize(800, 600)
    expect(manager.getActive()).toBeDefined()
    expect(manager.getMode()).toBe('perspective')
    manager.setMode('orthographic')
    expect(manager.getMode()).toBe('orthographic')
  })

  it('resizes cameras', () => {
    const manager = new CameraManager()
    manager.initialize(800, 600)
    manager.resize(1024, 768)
    expect(manager.getCameraState()).toBeDefined()
  })

  it('disposes cameras', () => {
    const manager = new CameraManager()
    manager.initialize(800, 600)
    manager.dispose()
    expect(manager.getActive()).toBeNull()
  })
})

describe('RendererManager', () => {
  it('skips initialization in non-browser environment', () => {
    const container = document.createElement('div')
    container.style.width = '800px'
    container.style.height = '600px'
    document.body.appendChild(container)
    const manager = new RendererManager()
    expect(() => {
      manager.initialize({
        width: 800,
        height: 600,
        pixelRatio: 1,
        viewId: 'view-3d',
        container,
      })
    }).toThrow()
    document.body.removeChild(container)
  })
})

describe('ControlsManager', () => {
  it('requires a perspective camera', () => {
    const container = document.createElement('div')
    const manager = new ControlsManager()
    const camera = new THREE.PerspectiveCamera(50, 800 / 600, 0.1, 10000)
    expect(() => {
      manager.initialize({
        width: 800,
        height: 600,
        pixelRatio: 1,
        viewId: 'view-3d',
        container,
        camera: camera as unknown as THREE.PerspectiveCamera,
      })
    }).not.toThrow()
    manager.dispose()
  })
})

describe('SelectionManager', () => {
  it('tracks selection state', () => {
    const manager = new SelectionManager()
    const state = manager.getState()
    expect(state.selectedIds).toEqual([])
    expect(state.hoveredId).toBeNull()
  })

  it('subscribes to state changes', () => {
    const manager = new SelectionManager()
    const listener = vi.fn()
    manager.subscribe(listener)
    manager.setHovered('element-1')
    expect(listener).toHaveBeenCalled()
  })
})

describe('ModelManager', () => {
  it('creates a root group', () => {
    const manager = new ModelManager()
    const scene = new THREE.Scene()
    manager.initialize(scene)
    expect(manager.getRoot()).not.toBeNull()
  })

  it('loads a demo model', () => {
    const manager = new ModelManager()
    const scene = new THREE.Scene()
    manager.initialize(scene)
    const model = DemoModelBuilder.build()
    manager.setModel(model)
    expect(manager.getModel()).not.toBeNull()
    expect(manager.getElements().length).toBeGreaterThan(0)
  })

  it('returns element metadata', () => {
    const manager = new ModelManager()
    const scene = new THREE.Scene()
    manager.initialize(scene)
    const model = DemoModelBuilder.build()
    manager.setModel(model)
    const first = manager.getElements()[0]
    const meta = manager.getElement(first.id)
    expect(meta).toBeDefined()
    expect(meta?.id).toBe(first.id)
  })
})

describe('GridManager', () => {
  it('attaches grid and axes to scene', () => {
    const manager = new GridManager()
    const scene = new THREE.Scene()
    manager.attach(scene, 100, 10)
    expect(manager.getGrid()).not.toBeNull()
    expect(manager.getAxes()).not.toBeNull()
    manager.detach()
  })
})

describe('LightingManager', () => {
  it('attaches lights to scene', () => {
    const manager = new LightingManager()
    const scene = new THREE.Scene()
    manager.attach(scene)
    const lights = manager.getLights()
    expect(lights.ambient).not.toBeNull()
    expect(lights.directional).not.toBeNull()
    expect(lights.hemisphere).not.toBeNull()
    manager.detach()
  })
})

describe('DemoModelBuilder', () => {
  it('builds a deterministic BIM model', () => {
    const model = DemoModelBuilder.build()
    expect(model.id).toBe('demo-model')
    expect(model.name).toBe('Demo BIM Model')
    expect(model.elements.length).toBeGreaterThan(0)
    expect(model.materials.length).toBeGreaterThan(0)
  })

  it('contains expected categories', () => {
    const model = DemoModelBuilder.build()
    const categories = new Set(model.elements.map((e) => e.category))
    expect(categories.has('Wall')).toBe(true)
    expect(categories.has('Floor')).toBe(true)
    expect(categories.has('Roof')).toBe(true)
    expect(categories.has('Column')).toBe(true)
    expect(categories.has('Beam')).toBe(true)
    expect(categories.has('Door')).toBe(true)
    expect(categories.has('Window')).toBe(true)
    expect(categories.has('Duct')).toBe(true)
    expect(categories.has('Pipe')).toBe(true)
  })
})
