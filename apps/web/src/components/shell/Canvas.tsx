'use client'

import React, { useEffect, useState } from 'react'
import { useShellStore } from '@/store/shellStore'
import { useDesignSlice } from '@/store/slices/designSlice'

export default function Canvas() {
  const { addNotification, activeViewTab } = useShellStore()
  const initialized = useDesignSlice((state) => state.initialized)
  const selectedElements = useDesignSlice((state) => state.getSelectedElements())
  const [engineState, setEngineState] = useState<string>('idle')

  useEffect(() => {
    setEngineState(initialized ? 'ready' : 'idle')
  }, [initialized])

  return (
    <div className="flex-1 flex items-center justify-center p-8">
      <div className="w-full h-full border border-datumbim-border rounded bg-datumbim-bg relative overflow-hidden">
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="text-center">
            <div className="text-6xl mb-4 opacity-20">🏗️</div>
            <div className="text-sm text-datumbim-textSecondary">
              {activeViewTab ? `View: ${activeViewTab}` : 'No active view'}
            </div>
            <div className="text-xs text-datumbim-textSecondary mt-1 opacity-60">
              DATUMBIM Canvas — engine: {engineState}
            </div>
            <div className="text-xs text-datumbim-textSecondary mt-1 opacity-60">
              Selected: {selectedElements.length} element{selectedElements.length !== 1 ? 's' : ''}
            </div>
          </div>
        </div>
        <div className="absolute top-3 left-3 text-[10px] text-datumbim-textSecondary opacity-60">
          Design Engine Foundation — TASK 003
        </div>
      </div>
    </div>
  )
}
