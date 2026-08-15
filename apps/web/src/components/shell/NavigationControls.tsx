'use client'

import React from 'react'
import { useShellStore } from '@/store/shellStore'
import { NavigationState } from '@/types/commands'
import { useDesignSlice } from '@/store/slices/designSlice'

const CONTROLS: { id: NavigationState['mode']; icon: string; title: string }[] = [
  { id: 'pan', icon: '✋', title: 'Pan' },
  { id: 'zoom', icon: '🔍', title: 'Zoom' },
  { id: 'orbit', icon: '🔄', title: 'Orbit' },
  { id: 'walk', icon: '🚶', title: 'Walk' },
  { id: 'fit', icon: '⛶', title: 'Fit to View' },
]

export default function NavigationControls() {
  const { addNotification, setNavigationMode, navigation } = useShellStore()
  const zoomExtents = useDesignSlice((state) => state.zoomExtents)
  const zoomIn = useDesignSlice((state) => state.zoomIn)
  const zoomOut = useDesignSlice((state) => state.zoomOut)

  const handleClick = (mode: NavigationState['mode']) => {
    setNavigationMode(mode)
    addNotification({ type: 'info', message: `Navigation mode: ${mode}` })
    if (mode === 'fit') {
      zoomExtents()
    }
  }

  return (
    <div className="absolute right-4 bottom-4 flex flex-col gap-1 bg-datumbim-surface border border-datumbim-border rounded shadow-lg p-1">
      {CONTROLS.map((control) => (
        <button
          key={control.id}
          onClick={() => handleClick(control.id)}
          className={`w-8 h-8 flex items-center justify-center rounded text-sm transition-colors ${
            navigation.mode === control.id
              ? 'bg-datumbim-accent text-white'
              : 'hover:bg-datumbim-border/50 text-datumbim-text'
          }`}
          title={control.title}
        >
          {control.icon}
        </button>
      ))}
      <div className="h-px bg-datumbim-border my-1" />
      <button
        onClick={() => zoomIn()}
        className="w-8 h-8 flex items-center justify-center rounded text-sm hover:bg-datumbim-border/50 text-datumbim-text"
        title="Zoom In"
      >
        +
      </button>
      <button
        onClick={() => zoomOut()}
        className="w-8 h-8 flex items-center justify-center rounded text-sm hover:bg-datumbim-border/50 text-datumbim-text"
        title="Zoom Out"
      >
        −
      </button>
      <div className="h-px bg-datumbim-border my-1" />
      <div className="text-[10px] text-datumbim-textSecondary text-center px-1">
        {navigation.status}
      </div>
    </div>
  )
}
