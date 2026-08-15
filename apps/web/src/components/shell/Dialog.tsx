'use client'

import React from 'react'
import { useShellStore } from '@/store/shellStore'

export default function Dialog() {
  const { dialogs, closeDialog } = useShellStore()

  if (dialogs.length === 0) return null

  return (
    <>
      {dialogs.map((dialog) => (
        <div key={dialog.id}>
          <div className="fixed inset-0 z-50 bg-black/50" onClick={() => closeDialog(dialog.id)} />
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4 pointer-events-none">
            <div className="bg-datumbim-surface border border-datumbim-border rounded-lg shadow-2xl w-full max-w-lg pointer-events-auto">
              <div className="flex items-center justify-between px-4 h-12 border-b border-datumbim-border">
                <h2 className="text-sm font-semibold text-datumbim-text">{dialog.title}</h2>
                <button
                  onClick={() => closeDialog(dialog.id)}
                  className="text-datumbim-textSecondary hover:text-datumbim-text text-sm"
                >
                  ×
                </button>
              </div>
              <div className="p-4 text-sm text-datumbim-textSecondary">
                {dialog.content || 'Dialog content placeholder'}
              </div>
              <div className="flex justify-end gap-2 px-4 py-3 border-t border-datumbim-border">
                <button
                  onClick={() => closeDialog(dialog.id)}
                  className="px-3 py-1.5 text-xs bg-datumbim-border text-datumbim-text rounded hover:bg-datumbim-border/80"
                >
                  Close
                </button>
              </div>
            </div>
          </div>
        </div>
      ))}
    </>
  )
}
