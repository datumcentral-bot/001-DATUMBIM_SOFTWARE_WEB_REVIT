'use client'

import React, { useState, useEffect, useCallback } from 'react'
import { useShellStore } from '@/store/shellStore'
import { apiClient } from '@/lib/apiClient'

interface RevitStatus {
  connection_state: string
  revit_version: string | null
  active_document: string | null
  active_view: string | null
  categories: any[]
  elements: any[]
  families: any[]
  levels: any[]
  views: any[]
  capabilities: any[]
}

export default function RevitIntelligence() {
  const { addNotification } = useShellStore()
  const [status, setStatus] = useState<RevitStatus | null>(null)
  const [loading, setLoading] = useState(false)
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null)
  const [selectedView, setSelectedView] = useState<string | null>(null)

  const loadStatus = useCallback(async () => {
    setLoading(true)
    try {
      const res = await apiClient.get<{ status: RevitStatus }>('/revit/status')
      if (res.error) throw new Error(res.error)
      setStatus(res.data?.status ?? null)
    } catch (e) {
      addNotification({ type: 'error', message: 'Failed to load Revit status' })
    } finally {
      setLoading(false)
    }
  }, [addNotification])

  useEffect(() => {
    loadStatus()
  }, [loadStatus])

  const connectionColor = (state: string) => {
    switch (state) {
      case 'connected':
        return 'text-green-400'
      case 'available':
        return 'text-yellow-400'
      case 'not_running':
        return 'text-red-400'
      case 'api_unavailable':
        return 'text-orange-400'
      default:
        return 'text-datumbim-textSecondary'
    }
  }

  return (
    <div className="h-full flex flex-col">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h2 className="text-sm font-semibold text-datumbim-text">Revit Intelligence</h2>
          <p className="text-xs text-datumbim-textSecondary">Object model and capability discovery</p>
        </div>
        <div className="flex gap-2">
          <button onClick={loadStatus} disabled={loading} className="text-[10px] px-2 py-1 bg-datumbim-border text-datumbim-text rounded hover:bg-datumbim-border/80 disabled:opacity-50">
            Refresh
          </button>
        </div>
      </div>
      <div className="flex-1 grid grid-cols-1 md:grid-cols-3 gap-3">
        <div className="bg-datumbim-surface border border-datumbim-border rounded p-3">
          <div className="text-[10px] font-semibold text-datumbim-textSecondary uppercase tracking-wider mb-2">Connection</div>
          {status && (
            <div className="space-y-1">
              <div className="text-xs text-datumbim-text">State: <span className={connectionColor(status.connection_state)}>{status.connection_state.toUpperCase()}</span></div>
              {status.revit_version && <div className="text-xs text-datumbim-textSecondary">Version: {status.revit_version}</div>}
              {status.active_document && <div className="text-xs text-datumbim-textSecondary">Document: {status.active_document}</div>}
              {status.active_view && <div className="text-xs text-datumbim-textSecondary">View: {status.active_view}</div>}
            </div>
          )}
          {!status && <div className="text-xs text-datumbim-textSecondary">No status available</div>}
        </div>
        <div className="bg-datumbim-surface border border-datumbim-border rounded p-3">
          <div className="text-[10px] font-semibold text-datumbim-textSecondary uppercase tracking-wider mb-2">Model Explorer</div>
          <div className="space-y-1">
            <div className="text-xs text-datumbim-text">Categories: {status?.categories?.length ?? 0}</div>
            <div className="text-xs text-datumbim-text">Elements: {status?.elements?.length ?? 0}</div>
            <div className="text-xs text-datumbim-text">Families: {status?.families?.length ?? 0}</div>
            <div className="text-xs text-datumbim-text">Levels: {status?.levels?.length ?? 0}</div>
            <div className="text-xs text-datumbim-text">Views: {status?.views?.length ?? 0}</div>
          </div>
        </div>
        <div className="bg-datumbim-surface border border-datumbim-border rounded p-3">
          <div className="text-[10px] font-semibold text-datumbim-textSecondary uppercase tracking-wider mb-2">Capabilities</div>
          <div className="space-y-1">
            {(status?.capabilities ?? []).slice(0, 8).map((cap: any) => (
              <div key={cap.capability_id} className="text-[10px] p-1 rounded border border-datumbim-border flex items-center justify-between">
                <span className="text-datumbim-text">{cap.name}</span>
                <span className={`text-[10px] ${cap.available ? 'text-green-400' : 'text-red-400'}`}>{cap.available ? 'ON' : 'OFF'}</span>
              </div>
            ))}
            {(status?.capabilities?.length ?? 0) === 0 && <div className="text-xs text-datumbim-textSecondary">No capabilities discovered</div>}
          </div>
        </div>
      </div>
    </div>
  )
}
