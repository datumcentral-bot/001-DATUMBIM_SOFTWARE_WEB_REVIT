'use client'

import React, { useRef, useEffect, useCallback, useState } from 'react'
import { useShellStore } from '@/store/shellStore'
import { useDesignSlice } from '@/store/slices/designSlice'
import { ViewerEngine } from '@/lib/viewer'

export default function Canvas() {
  const containerRef = useRef<HTMLDivElement>(null)
  const engineRef = useRef<ViewerEngine | null>(null)
  const { activeView } = useShellStore()
  const selectedIds = useDesignSlice((state) => state.getSelectedElements())
  const setViewerEngine = useDesignSlice((state) => state.setViewerEngine)
  const loadDemoModel = useDesignSlice((state) => state.loadDemoModel)
  const setRenderMode = useDesignSlice((state) => state.setRenderMode)
  const initialized = useDesignSlice((state) => state.initialized)
  const addNotification = useShellStore((state) => state.addNotification)
  const [error, setError] = useState<string | null>(null)
  const [webGLAvailable, setWebGLAvailable] = useState(true)

  useEffect(() => {
    if (!containerRef.current || engineRef.current) return
    let cancelled = false
    ;(async () => {
      try {
        const engine = new ViewerEngine()
        engineRef.current = engine
        engine.attachDesignEngine(useDesignSlice.getState().engine)
        engine.initialize(containerRef.current!)
        if (cancelled) return
        setViewerEngine(engine)
        loadDemoModel()
        addNotification({ type: 'info', message: '3D Viewer initialized' })
      } catch (e) {
        if (cancelled) return
        const message = e instanceof Error ? e.message : 'Failed to initialize viewer'
        setError(message)
        setWebGLAvailable(false)
      }
    })()
    return () => {
      cancelled = true
      engineRef.current?.dispose()
      engineRef.current = null
      setViewerEngine(null)
    }
  }, [setViewerEngine, loadDemoModel, addNotification])

  useEffect(() => {
    if (!engineRef.current) return
    engineRef.current.setRenderMode('shaded')
  }, [initialized])

  const handleWheel = useCallback((e: React.WheelEvent) => {
    e.preventDefault()
  }, [])

  return (
    <div className="flex-1 relative bg-datumbim-bg overflow-hidden">
      <div ref={containerRef} className="absolute inset-0" onWheel={handleWheel} />
      {!webGLAvailable && (
        <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
          <div className="text-center pointer-events-auto">
            <div className="text-6xl mb-4 opacity-20 text-datumbim-text">⚠️</div>
            <div className="text-lg font-medium text-datumbim-text mb-2">WebGL Unavailable</div>
            <div className="text-xs text-datumbim-textSecondary mb-4">
              {error || 'Your browser or environment does not support WebGL.'}
            </div>
            <div className="text-xs text-datumbim-textSecondary">
              The 3D viewer requires WebGL. Please use a modern browser with hardware acceleration enabled.
            </div>
          </div>
        </div>
      )}
      <div className="absolute top-4 left-4 flex flex-col gap-2 pointer-events-none">
        <div className="bg-datumbim-surface/90 backdrop-blur border border-datumbim-border rounded p-2 pointer-events-auto">
          <div className="text-[10px] font-semibold text-datumbim-textSecondary uppercase tracking-wider mb-2">View Mode</div>
          <div className="flex flex-col gap-1">
            <button onClick={() => setRenderMode('shaded')} className="text-xs px-2 py-1 bg-datumbim-border hover:bg-datumbim-border/80 rounded text-datumbim-text text-left">
              Shaded
            </button>
            <button onClick={() => setRenderMode('wireframe')} className="text-xs px-2 py-1 bg-datumbim-border hover:bg-datumbim-border/80 rounded text-datumbim-text text-left">
              Wireframe
            </button>
          </div>
        </div>
        <div className="bg-datumbim-surface/90 backdrop-blur border border-datumbim-border rounded p-2 pointer-events-auto">
          <div className="text-[10px] font-semibold text-datumbim-textSecondary uppercase tracking-wider mb-2">View Controls</div>
          <div className="flex flex-col gap-1">
            <button onClick={() => useDesignSlice.getState().zoomIn()} className="text-xs px-2 py-1 bg-datumbim-border hover:bg-datumbim-border/80 rounded text-datumbim-text text-left">
              Zoom In
            </button>
            <button onClick={() => useDesignSlice.getState().zoomOut()} className="text-xs px-2 py-1 bg-datumbim-border hover:bg-datumbim-border/80 rounded text-datumbim-text text-left">
              Zoom Out
            </button>
            <button onClick={() => useDesignSlice.getState().fitToView()} className="text-xs px-2 py-1 bg-datumbim-border hover:bg-datumbim-border/80 rounded text-datumbim-text text-left">
              Fit
            </button>
            <button onClick={() => {
              engineRef.current?.setCameraOrientation('front')
              useDesignSlice.getState().zoomExtents()
            }} className="text-xs px-2 py-1 bg-datumbim-border hover:bg-datumbim-border/80 rounded text-datumbim-text text-left">
              Reset
            </button>
          </div>
        </div>
      </div>
      <div className="absolute bottom-4 left-4 bg-datumbim-surface/90 backdrop-blur border border-datumbim-border rounded px-3 py-2 pointer-events-none">
        <div className="text-[10px] text-datumbim-textSecondary">
          Left-click: Select | Middle-click: Pan | Right-click: Orbit | Scroll: Zoom
        </div>
      </div>
      {selectedIds.length > 0 && (
        <div className="absolute top-4 right-4 bg-datumbim-surface/90 backdrop-blur border border-datumbim-border rounded px-3 py-2 pointer-events-none">
          <div className="text-xs text-datumbim-textSecondary">
            {selectedIds.length} element{selectedIds.length !== 1 ? 's' : ''} selected
          </div>
        </div>
      )}
    </div>
  )
}
