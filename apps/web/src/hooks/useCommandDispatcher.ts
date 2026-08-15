'use client'

import React, { useCallback, useEffect, useRef } from 'react'
import { ALL_COMMANDS, CommandDefinition } from '@/constants/commands'

type CommandHandler = (command: CommandDefinition) => void

const registeredHandlers = new Map<string, CommandHandler[]>()

export function registerCommandHandler(action: string, handler: CommandHandler) {
  const handlers = registeredHandlers.get(action) || []
  handlers.push(handler)
  registeredHandlers.set(action, handlers)
}

export function unregisterCommandHandler(action: string, handler: CommandHandler) {
  const handlers = registeredHandlers.get(action) || []
  const next = handlers.filter((h) => h !== handler)
  if (next.length === 0) {
    registeredHandlers.delete(action)
  } else {
    registeredHandlers.set(action, next)
  }
}

export function dispatchCommand(command: CommandDefinition) {
  const handlers = registeredHandlers.get(command.action) || []
  if (handlers.length === 0) {
    console.warn(`[CommandDispatcher] No handlers registered for action: ${command.action}`)
    return
  }
  handlers.forEach((handler) => {
    try {
      handler(command)
    } catch (error) {
      console.error(`[CommandDispatcher] Handler failed for ${command.action}:`, error)
    }
  })
}

export function useCommandDispatcher() {
  const handlersRef = useRef<CommandHandler[]>([])

  const register = useCallback((action: string, handler: CommandHandler) => {
    registerCommandHandler(action, handler)
    handlersRef.current.push(handler)
    return () => unregisterCommandHandler(action, handler)
  }, [])

  const dispatch = useCallback((command: CommandDefinition) => {
    dispatchCommand(command)
  }, [])

  useEffect(() => {
    return () => {
      handlersRef.current.forEach((handler, index) => {
        const action = ALL_COMMANDS[index]?.action
        if (action) unregisterCommandHandler(action, handler)
      })
      handlersRef.current = []
    }
  }, [])

  return { register, dispatch }
}
