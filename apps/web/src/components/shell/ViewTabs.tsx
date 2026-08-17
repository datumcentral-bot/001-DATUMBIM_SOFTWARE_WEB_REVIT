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
  'applications': '🖥️',
  'sessions': '🔗',
  'observation': '👁️',
  'control': '🎮',
  'execution': '⚡',
  'workflows': '🔀',
  'ai': '🤖',
  'planner': '📝',
  'revit': '🏗️',
  'live-application': '🖥️',
  'integrations': '🔌',
}

export default function ViewTabs({ activeTab, onTabChange }: { activeTab: string | null; onTabChange: (tabId: string) => void }) {
  const { views, setActiveView, pushNavigation } = useShellStore()
  const setDesignActiveView = useDesignSlice((state) => state.setActiveView)
  const tabs = views.length > 0 ? views : DEFAULT_VIEW_TABS

  const handleTabClick = (tabId: string, label: string) => {
    setActiveView(tabId)
    setDesignActiveView(tabId)
    pushNavigation(label)
    onTabChange(tabId)
  }

  return (
    <div className="h-9 bg-datumbim-ribbon border-b border-datumbim-border flex items-end px-1 overflow-x-auto">
      {tabs.map((tab) => {
        const tabLabel = 'label' in tab ? tab.label : tab.name
        return (
          <button
            key={tab.id}
            onClick={() => handleTabClick(tab.id, tabLabel)}
            className={`flex items-center gap-2 px-3 py-1.5 text-xs border-t-2 transition-colors ${
              activeTab === tab.id
                ? 'border-datumbim-accent text-datumbim-text bg-datumbim-surface/50'
                : 'border-transparent text-datumbim-textSecondary hover:text-datumbim-text hover:bg-datumbim-surface/30'
            }`}
          >
            <span className="text-[10px]">{VIEW_ICONS[tab.type] || '📋'}</span>
            <span className="truncate max-w-[120px]">{tabLabel}</span>
          </button>
        )
      })}
    </div>
  )
}
