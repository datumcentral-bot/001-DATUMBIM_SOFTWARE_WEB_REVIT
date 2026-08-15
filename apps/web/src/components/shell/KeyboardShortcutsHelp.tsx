'use client'

import React from 'react'
import { useShellStore } from '@/store/shellStore'
import { ALL_COMMANDS, CommandDefinition } from '@/constants/commands'

export default function KeyboardShortcutsHelp() {
  const { openDialog, closeDialog } = useShellStore()
  const shortcuts = ALL_COMMANDS.filter((cmd: CommandDefinition) => cmd.shortcut)

  const openShortcuts = () => {
    openDialog({
      id: 'keyboard-shortcuts',
      title: 'Keyboard Shortcuts',
      content: (
        <div className="max-h-96 overflow-auto">
          <div className="grid grid-cols-2 gap-2 text-xs">
            {shortcuts.map((cmd) => (
              <div key={cmd.id} className="flex items-center justify-between py-1">
                <span className="text-datumbim-text">{cmd.label}</span>
                <span className="text-datumbim-textSecondary bg-datumbim-bg px-1.5 py-0.5 rounded text-[10px]">
                  {cmd.shortcut}
                </span>
              </div>
            ))}
          </div>
        </div>
      ),
    })
  }

  const openShortcutsRef = React.useRef(openShortcuts)
  openShortcutsRef.current = openShortcuts

  React.useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.shiftKey && e.key === '?') {
        e.preventDefault()
        openShortcutsRef.current()
      }
    }
    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [])

  return null
}
