'use client'

import React from 'react'
import { useShellStore } from '@/store/shellStore'
import { COMMAND_CATEGORIES } from '@/constants/commands'

export default function QuickAccessToolbar() {
  const { addNotification, executeCommand } = useShellStore()
  const fileCommands = COMMAND_CATEGORIES.find((c) => c.id === 'file')?.commands.slice(0, 5) || []

  return (
    <div className="h-8 bg-datumbim-surface border-b border-datumbim-border flex items-center px-2 gap-1">
      {fileCommands.map((cmd) => (
        <button
          key={cmd.id}
          onClick={() => executeCommand(cmd.id)}
          className="h-6 w-8 flex items-center justify-center rounded hover:bg-datumbim-border/50 text-datumbim-text text-sm"
          title={`${cmd.label} (${cmd.shortcut})`}
        >
          {cmd.id === 'new-project' && '📄'}
          {cmd.id === 'open' && '📂'}
          {cmd.id === 'save' && '💾'}
          {cmd.id === 'undo' && '↩️'}
          {cmd.id === 'redo' && '↪️'}
        </button>
      ))}
      <div className="w-px h-4 bg-datumbim-border mx-1" />
      <span className="text-[10px] text-datumbim-textSecondary">Shell ready</span>
    </div>
  )
}
