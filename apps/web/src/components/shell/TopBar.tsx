'use client'

import React from 'react'

export default function TopBar() {
  return (
    <div className="h-9 bg-datumbim-ribbon border-b border-datumbim-border flex items-center px-2 select-none">
      <div className="flex items-center gap-2">
        <span className="font-bold text-sm text-datumbim-text tracking-wide">DATUMBIM</span>
        <span className="text-[10px] text-datumbim-textSecondary bg-datumbim-surface px-1.5 py-0.5 rounded border border-datumbim-border">
          WEB REVIT
        </span>
      </div>
      <div className="ml-auto flex items-center gap-1">
        <span className="text-[11px] text-datumbim-textSecondary">TASK 002 — Application Shell</span>
      </div>
    </div>
  )
}
