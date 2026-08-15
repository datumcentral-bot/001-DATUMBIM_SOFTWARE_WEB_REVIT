'use client'

import React from 'react'
import { DEFAULT_VIEW_TABS } from '@/constants/shell'
import { useShellStore } from '@/store/shellStore'
import { useDesignSlice } from '@/store/slices/designSlice'

const VIEW_ICONS: Record<string, string> = {
  '3d': '🎲',
  'floor-plan': '📋',
  'ceiling-plan': '📋',
  'elevation': '📊',
  'section': '✂️',
  'detail': '🔍',
  'schedule': '📊',
  'sheet': '📄',
  'drafting': '✏️',
  'browser': '📂',
  'model': '📦',
}

export default function ViewTabs() {
  const { activeViewTab, setActiveViewTab, pushNavigation } = useShellStore()
  const setActiveView = useDesignSlice((state) => state.setActiveView)
  const tabs = DEFAULT_VIEW_TABS

  const handleTabClick = (tabId: string, label: string) => {
    setActiveViewTab(tabId)
    setActiveView(tabId)
    pushNavigation(label)
  }

  return (
    <div className="h-9 bg-datumbim-ribbon border-b border-datumbim-border flex items-end px-1 overflow-x-auto">
      {tabs.map((tab) => (
        <button
          key={tab.id}
          onClick={() => handleTabClick(tab.id, tab.label)}
          className={`flex items-center gap-2 px-3 py-1.5 text-xs border-t-2 transition-colors ${
            activeViewTab === tab.id
              ? 'border-datumbim-accent text-datumbim-text bg-datumbim-surface/50'
              : 'border-transparent text-datumbim-textSecondary hover:text-datumbim-text hover:bg-datumbim-surface/30'
          }`}
        >
          <span className="text-[10px]">{VIEW_ICONS[tab.type] || '📋'}</span>
          <span className="truncate max-w-[120px]">{tab.label}</span>
        </button>
      ))}
      <button className="ml-auto px-2 py-1 text-[10px] text-datumbim-textSecondary hover:text-datumbim-text">
        +
      </button>
    </div>
  )
}
