'use client'

import React from 'react'
import { useShellStore } from '@/store/shellStore'

export default function CommandLauncher() {
  const { commandPaletteOpen, setCommandPaletteOpen } = useShellStore()

  if (!commandPaletteOpen) return null

  return (
    <div className="fixed inset-0 z-50 flex items-start justify-center pt-[15vh]">
      <div className="absolute inset-0 bg-black/40" onClick={() => setCommandPaletteOpen(false)} />
      <div className="relative w-full max-w-xl bg-datumbim-surface border border-datumbim-border rounded-lg shadow-2xl overflow-hidden">
        <div className="px-4 h-12 border-b border-datumbim-border flex items-center gap-2">
          <span className="text-datumbim-textSecondary">⌘</span>
          <span className="text-sm text-datumbim-textSecondary">Command palette placeholder</span>
        </div>
        <div className="p-4 text-xs text-datumbim-textSecondary">
          Command launcher framework initialized. Wire to feature registry in TASK 005.
        </div>
      </div>
    </div>
  )
}
