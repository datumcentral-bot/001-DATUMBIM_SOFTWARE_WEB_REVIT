'use client'

import React from 'react'
import { RIBBON_TABS, RIBBON_PANELS } from '@/constants/shell'
import { useShellStore } from '@/store/shellStore'
import { ALL_COMMANDS } from '@/constants/commands'

export default function Ribbon() {
  const { activeRibbonTab, setActiveRibbonTab, addNotification, executeCommand } = useShellStore()
  const panels = RIBBON_PANELS[activeRibbonTab] || []

  const handleCommand = (commandId: string) => {
    executeCommand(commandId)
  }

  return (
    <div className="bg-datumbim-ribbon border-b border-datumbim-border select-none">
      <div className="flex items-end px-1 pt-1">
        {RIBBON_TABS.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveRibbonTab(tab.id)}
            className={`px-4 py-1.5 text-xs font-medium border-t-2 transition-colors ${
              activeRibbonTab === tab.id
                ? 'border-datumbim-accent text-datumbim-text bg-datumbim-surface/50'
                : 'border-transparent text-datumbim-textSecondary hover:text-datumbim-text hover:bg-datumbim-surface/30'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>
      {panels.length > 0 && (
        <div className="flex items-start gap-6 px-2 pb-2 overflow-x-auto">
          {panels.map((panel) => (
            <div key={panel.id} className="flex flex-col gap-1 min-w-[100px]">
              <div className="text-[10px] font-semibold text-datumbim-textSecondary mb-1 uppercase tracking-wider">
                {panel.label}
              </div>
              <div className="flex flex-wrap gap-1">
                {panel.items.map((item) => (
                  <button
                    key={item.id}
                    onClick={() => handleCommand(item.id)}
                    className="flex flex-col items-center justify-center w-14 h-14 rounded border border-transparent hover:border-datumbim-border hover:bg-datumbim-surface/50 text-datumbim-text gap-1 group"
                    title={item.label}
                  >
                    <span className="text-lg leading-none group-hover:scale-110 transition-transform">{item.icon}</span>
                    <span className="text-[10px] leading-tight text-center line-clamp-2">{item.label}</span>
                  </button>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
