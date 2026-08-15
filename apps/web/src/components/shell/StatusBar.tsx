'use client'

import React from 'react'
import { useShellStore } from '@/store/shellStore'
import { useDesignSlice } from '@/store/slices/designSlice'

export default function StatusBar() {
  const { activeView, project } = useShellStore()
  const selectedIds = useDesignSlice((state) => state.getSelectedElements())
  const viewerEngine = useDesignSlice((state) => state.getViewerEngine())
  const viewerState = viewerEngine?.getState()

  return (
    <div className="h-7 bg-datumbim-ribbon border-t border-datumbim-border flex items-center px-3 text-[11px] text-datumbim-textSecondary select-none">
      <div className="flex items-center gap-4">
        <span className="flex items-center gap-1.5">
          <span className="w-2 h-2 rounded-full bg-green-500" />
          READY
        </span>
        {activeView ? (
          <span>View: <span className="text-datumbim-text">{activeView.name}</span></span>
        ) : (
          <span>No active view</span>
        )}
        {selectedIds.length > 0 && (
          <span>{selectedIds.length} selected</span>
        )}
        <span>Nav: {viewerState?.cameraMode ?? 'Pan'}</span>
        <span>Render: {viewerState?.renderMode ?? 'shaded'}</span>
        <span>Units: mm</span>
      </div>
      <div className="ml-auto flex items-center gap-4">
        {project.isOpen && project.name && (
          <span className="text-datumbim-text">
            {project.name}
            {project.isModified && <span className="ml-1 text-yellow-500">●</span>}
          </span>
        )}
        <span>TASK 007F</span>
      </div>
    </div>
  )
}
