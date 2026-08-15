'use client'

import React from 'react'
import { useShellStore } from '@/store/shellStore'

export default function StatusBar() {
  const { activeViewTab, navigation, commandHistory, addNotification } = useShellStore()
  const historyLength = commandHistory.length

  return (
    <div className="h-7 bg-datumbim-ribbon border-t border-datumbim-border flex items-center px-3 text-[11px] text-datumbim-textSecondary select-none">
      <div className="flex items-center gap-4">
        <span className="flex items-center gap-1">
          <span className="w-2 h-2 rounded-full bg-green-500" />
          READY
        </span>
        {activeViewTab && <span>View: {activeViewTab}</span>}
        <span>Nav: {navigation.mode}</span>
        <span>History: {historyLength}</span>
      </div>
      <div className="ml-auto flex items-center gap-4">
        <button
          onClick={() => addNotification({ type: 'info', message: 'Task 002 shell active' })}
          className="hover:text-datumbim-text"
        >
          TASK 002
        </button>
      </div>
    </div>
  )
}
