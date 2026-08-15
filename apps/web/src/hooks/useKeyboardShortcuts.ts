'use client'

import { useEffect, useCallback } from 'react'

type ShortcutHandler = (commandId: string) => void

const listeners = new Set<ShortcutHandler>()

function normalizeShortcut(shortcut: string): string {
  return shortcut
    .replace(/Ctrl/g, 'Control')
    .replace(/Alt/g, 'Alt')
    .replace(/Shift/g, 'Shift')
    .replace(/Del/g, 'Delete')
}

export function useKeyboardShortcuts() {
  const handleKeyDown = useCallback((event: KeyboardEvent) => {
    const modifiers: string[] = []
    if (event.ctrlKey || event.metaKey) modifiers.push('Ctrl')
    if (event.altKey) modifiers.push('Alt')
    if (event.shiftKey) modifiers.push('Shift')

    const key = event.key === ' ' ? 'Space' : event.key
    const shortcut = normalizeShortcut([...modifiers, key].join('+'))

    listeners.forEach((handler) => {
      try {
        handler(shortcut)
      } catch (error) {
        console.error('[KeyboardShortcuts] Handler failed:', error)
      }
    })
  }, [])

  useEffect(() => {
    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [handleKeyDown])

  const subscribe = useCallback((handler: ShortcutHandler) => {
    listeners.add(handler)
    return () => listeners.delete(handler)
  }, [])

  return { subscribe }
}
