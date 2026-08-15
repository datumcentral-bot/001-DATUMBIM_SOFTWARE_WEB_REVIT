'use client'

import React, { useRef, useEffect, useState } from 'react'
import { useShellStore } from '@/store/shellStore'
import { useDesignSlice } from '@/store/slices/designSlice'

interface ViewportState {
  zoom: number
  panX: number
  panY: number
  mode: 'orbit' | 'pan' | 'select'
}

export default function Canvas() {
  const { addNotification, activeView, setActiveView, views } = useShellStore()
  const selectedIds = useDesignSlice((state) => state.getSelectedElements())
  const [viewport, setViewport] = useState<ViewportState>({
    zoom: 1,
    panX: 0,
    panY: 0,
    mode: 'orbit',
  })
  const [isDragging, setIsDragging] = useState(false)
  const [dragStart, setDragStart] = useState({ x: 0, y: 0 })
  const containerRef = useRef<HTMLDivElement>(null)

  const handleMouseDown = (e: React.MouseEvent) => {
    if (e.button === 1 || (e.button === 0 && viewport.mode === 'pan')) {
      setIsDragging(true)
      setDragStart({ x: e.clientX - viewport.panX, y: e.clientY - viewport.panY })
    }
  }

  const handleMouseMove = (e: React.MouseEvent) => {
    if (isDragging) {
      setViewport((v) => ({
        ...v,
        panX: e.clientX - dragStart.x,
        panY: e.clientY - dragStart.y,
      }))
    }
  }

  const handleMouseUp = () => {
    setIsDragging(false)
  }

  const handleWheel = (e: React.WheelEvent) => {
    e.preventDefault()
    const delta = e.deltaY > 0 ? 0.9 : 1.1
    setViewport((v) => ({
      ...v,
      zoom: Math.min(Math.max(v.zoom * delta, 0.1), 10),
    }))
  }

  const handleClick = (e: React.MouseEvent<HTMLDivElement>) => {
    if (viewport.mode === 'select') {
      const target = e.target as HTMLElement
      const rect = target.getBoundingClientRect()
      const x = e.clientX - rect.left
      const y = e.clientY - rect.top
      addNotification({ type: 'info', message: `Selected element at (${x.toFixed(0)}, ${y.toFixed(0)})` })
    }
  }

  const fitToView = () => {
    setViewport({ zoom: 1, panX: 0, panY: 0, mode: viewport.mode })
    addNotification({ type: 'info', message: 'Fit to view' })
  }

  const resetView = () => {
    setViewport({ zoom: 1, panX: 0, panY: 0, mode: viewport.mode })
    addNotification({ type: 'info', message: 'View reset' })
  }

  return (
    <div className="flex-1 relative bg-datumbim-bg overflow-hidden">
      <div
        ref={containerRef}
        className="absolute inset-0 cursor-crosshair"
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onMouseLeave={handleMouseUp}
        onWheel={handleWheel}
        onClick={handleClick}
      >
        <div
          className="absolute inset-0 flex items-center justify-center"
          style={{
            transform: `translate(${viewport.panX}px, ${viewport.panY}px) scale(${viewport.zoom})`,
            transition: isDragging ? 'none' : 'transform 0.1s ease-out',
          }}
        >
          <div className="relative w-full h-full max-w-4xl max-h-4xl">
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="text-center">
                <div className="text-8xl mb-6 opacity-10 font-light text-datumbim-text">🏗️</div>
                <div className="text-lg font-medium text-datumbim-text mb-2">
                  {activeView ? activeView.name : 'No Active View'}
                </div>
                <div className="text-xs text-datumbim-textSecondary mb-1">
                  DATUMBIM 3D Viewport
                </div>
                <div className="text-xs text-datumbim-textSecondary opacity-60">
                  Zoom: {(viewport.zoom * 100).toFixed(0)}% | Mode: {viewport.mode}
                </div>
                {selectedIds.length > 0 && (
                  <div className="text-xs text-datumbim-textSecondary mt-2">
                    {selectedIds.length} element{selectedIds.length !== 1 ? 's' : ''} selected
                  </div>
                )}
              </div>
            </div>

            <div className="absolute top-4 left-4 flex flex-col gap-2">
              <div className="bg-datumbim-surface/90 backdrop-blur border border-datumbim-border rounded p-2">
                <div className="text-[10px] font-semibold text-datumbim-textSecondary uppercase tracking-wider mb-2">View Controls</div>
                <div className="flex flex-col gap-1">
                  <button onClick={() => setViewport((v) => ({ ...v, zoom: Math.min(v.zoom * 1.2, 10) }))} className="text-xs px-2 py-1 bg-datumbim-border hover:bg-datumbim-border/80 rounded text-datumbim-text text-left">
                    Zoom In
                  </button>
                  <button onClick={() => setViewport((v) => ({ ...v, zoom: Math.max(v.zoom * 0.8, 0.1) }))} className="text-xs px-2 py-1 bg-datumbim-border hover:bg-datumbim-border/80 rounded text-datumbim-text text-left">
                    Zoom Out
                  </button>
                  <button onClick={fitToView} className="text-xs px-2 py-1 bg-datumbim-border hover:bg-datumbim-border/80 rounded text-datumbim-text text-left">
                    Fit
                  </button>
                  <button onClick={resetView} className="text-xs px-2 py-1 bg-datumbim-border hover:bg-datumbim-border/80 rounded text-datumbim-text text-left">
                    Reset
                  </button>
                </div>
              </div>
            </div>

            <div className="absolute bottom-4 left-4 bg-datumbim-surface/90 backdrop-blur border border-datumbim-border rounded px-3 py-2">
              <div className="text-[10px] text-datumbim-textSecondary">
                Scroll to zoom | Middle-click to pan | Click to select
              </div>
            </div>

            <div className="absolute top-4 right-4 grid grid-cols-3 gap-1">
              {['Top', 'Front', 'Right', 'Left', 'Back', 'Bottom'].map((view) => (
                <button
                  key={view}
                  onClick={() => addNotification({ type: 'info', message: `View: ${view}` })}
                  className="text-[10px] px-2 py-1 bg-datumbim-surface/90 backdrop-blur border border-datumbim-border rounded hover:bg-datumbim-border/50 text-datumbim-textSecondary hover:text-datumbim-text"
                >
                  {view}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
