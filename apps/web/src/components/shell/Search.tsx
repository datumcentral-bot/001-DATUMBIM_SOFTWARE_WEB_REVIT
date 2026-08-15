'use client'

import React, { useState, useEffect, useRef } from 'react'
import { useShellStore } from '@/store/shellStore'
import { ALL_COMMANDS, CommandDefinition } from '@/constants/commands'

export default function Search() {
  const [query, setQuery] = useState('')
  const [isOpen, setIsOpen] = useState(false)
  const inputRef = useRef<HTMLInputElement>(null)
  const { setCommandPaletteOpen, executeCommand } = useShellStore()

  const filtered = ALL_COMMANDS.filter((cmd: CommandDefinition) =>
    cmd.label.toLowerCase().includes(query.toLowerCase())
  )

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault()
        setIsOpen((prev) => !prev)
        setCommandPaletteOpen(!isOpen)
      }
      if (e.key === 'Escape') {
        setIsOpen(false)
        setCommandPaletteOpen(false)
      }
    }
    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [isOpen, setCommandPaletteOpen])

  if (!isOpen) {
    return (
      <button
        onClick={() => setIsOpen(true)}
        className="h-7 px-3 bg-datumbim-surface border border-datumbim-border rounded text-xs text-datumbim-textSecondary hover:text-datumbim-text flex items-center gap-2 min-w-[200px]"
      >
        <span>🔍</span>
        <span className="flex-1 text-left">Search commands...</span>
        <span className="text-[10px] opacity-60">Ctrl+K</span>
      </button>
    )
  }

  return (
    <div className="fixed inset-0 z-50 flex items-start justify-center pt-[15vh]">
      <div className="w-full max-w-xl bg-datumbim-surface border border-datumbim-border rounded-lg shadow-2xl overflow-hidden">
        <div className="flex items-center gap-2 px-4 h-12 border-b border-datumbim-border">
          <span className="text-datumbim-textSecondary">🔍</span>
          <input
            ref={inputRef}
            autoFocus
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Type a command..."
            className="flex-1 bg-transparent text-sm text-datumbim-text outline-none"
          />
          <button
            onClick={() => setIsOpen(false)}
            className="text-datumbim-textSecondary hover:text-datumbim-text text-sm"
          >
            ESC
          </button>
        </div>
        <div className="max-h-80 overflow-auto py-2">
          {filtered.length === 0 && (
            <div className="px-4 py-3 text-xs text-datumbim-textSecondary">No results</div>
          )}
          {filtered.map((cmd) => (
            <button
              key={cmd.id}
              onClick={() => {
                executeCommand(cmd.id)
                setIsOpen(false)
              }}
              className="w-full flex items-center justify-between px-4 py-2 text-sm text-datumbim-text hover:bg-datumbim-border/40"
            >
              <span>{cmd.label}</span>
              {cmd.shortcut && (
                <span className="text-[10px] text-datumbim-textSecondary bg-datumbim-bg px-1.5 py-0.5 rounded">
                  {cmd.shortcut}
                </span>
              )}
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}
