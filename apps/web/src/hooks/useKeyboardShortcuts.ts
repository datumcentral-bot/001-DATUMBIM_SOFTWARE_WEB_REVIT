import { useEffect, useRef } from 'react'
import { useShellStore } from '@/store/shellStore'
import { ALL_COMMANDS, CommandDefinition } from '@/constants/commands'

export function useKeyboardShortcuts() {
  const { executeCommand, closeDialog } = useShellStore()
  const commandsRef = useRef<Map<string, CommandDefinition>>(new Map())

  useEffect(() => {
    commandsRef.current = new Map(ALL_COMMANDS.map((cmd) => [cmd.shortcut || '', cmd]))
  }, [])

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      const isMod = e.metaKey || e.ctrlKey
      if (!isMod) return

      const parts = [e.key.toUpperCase()]
      if (e.shiftKey) parts.push('SHIFT')
      const combo = parts.join('+')

      const cmd = commandsRef.current.get(combo)
      if (!cmd) return

      e.preventDefault()
      executeCommand(cmd.action)
    }

    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [executeCommand])
}
