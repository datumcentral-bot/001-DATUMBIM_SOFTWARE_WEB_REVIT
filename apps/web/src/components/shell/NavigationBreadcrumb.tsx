'use client'

import React from 'react'
import { useShellStore } from '@/store/shellStore'

export default function NavigationBreadcrumb() {
  const { navigationStack, popNavigation, activeViewTab } = useShellStore()
  const displayStack = activeViewTab ? [...navigationStack, activeViewTab] : navigationStack

  if (displayStack.length === 0) return null

  return (
    <div className="h-7 bg-datumbim-surface border-b border-datumbim-border flex items-center px-3 gap-1 text-[11px] text-datumbim-textSecondary">
      <button
        onClick={() => popNavigation()}
        disabled={displayStack.length <= 1}
        className="hover:text-datumbim-text disabled:opacity-40 disabled:cursor-not-allowed"
      >
        ← Back
      </button>
      <span className="text-datumbim-border">|</span>
      {displayStack.map((item, index) => (
        <React.Fragment key={index}>
          {index > 0 && <span className="text-datumbim-border">›</span>}
          <span className={index === displayStack.length - 1 ? 'text-datumbim-text' : ''}>{item}</span>
        </React.Fragment>
      ))}
    </div>
  )
}
