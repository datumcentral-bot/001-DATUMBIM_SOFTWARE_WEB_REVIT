'use client'

import React, { useState, useEffect, useCallback } from 'react'
import { useShellStore } from '@/store/shellStore'
import type { ApplicationSession } from '@/lib/connectors/types/ConnectorTypes'

interface ActionRecord {
  action_id: string
  session_id: string
  application_id: string
  action_type: string
  status: string
  result: string
  timestamp: string
}

export default function ControlScreen() {
  const { addNotification } = useShellStore()
  const [sessions, setSessions] = useState<ApplicationSession[]>([])
  const [selectedSessionId, setSelectedSessionId] = useState<string | null>(null)
  const [actions, setActions] = useState<ActionRecord[]>([])
  const [actionType, setActionType] = useState('mouse_click')
  const [parameters, setParameters] = useState('{"x": 100, "y": 100}')
  const [riskLevel, setRiskLevel] = useState('low')
  const [approvalRequired, setApprovalRequired] = useState(false)
  const [dryRun, setDryRun] = useState(true)
  const [loading, setLoading] = useState(false)

  const loadSessions = useCallback(async () => {
    setLoading(true)
    try {
      const response = await fetch('/api/connectors/sessions')
      if (!response.ok) throw new Error('Failed to load sessions')
      const data = await response.json()
      setSessions(data.sessions ?? [])
    } catch (e) {
      addNotification({ type: 'error', message: 'Failed to load sessions' })
    } finally {
      setLoading(false)
    }
  }, [addNotification])

  useEffect(() => {
    loadSessions()
  }, [loadSessions])

  const handleExecute = async () => {
    if (!selectedSessionId) return
    setLoading(true)
    try {
      const response = await fetch('/api/control/actions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          action_id: `action-${Date.now()}`,
          session_id: selectedSessionId,
          application_id: sessions.find(s => s.id === selectedSessionId)?.applicationId ?? '',
          action_type: actionType,
          parameters: JSON.parse(parameters),
          requested_by: 'user',
          risk_level: riskLevel,
          approval_required: approvalRequired,
          dry_run: dryRun,
        }),
      })
      if (!response.ok) throw new Error('Failed to execute action')
      const data = await response.json()
      setActions((prev) => [data.action, ...prev])
      addNotification({ type: 'success', message: `Action ${dryRun ? 'dry-run' : 'executed'}: ${actionType}` })
    } catch (e) {
      addNotification({ type: 'error', message: 'Failed to execute action' })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="h-full flex flex-col">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h2 className="text-sm font-semibold text-datumbim-text">Control</h2>
          <p className="text-xs text-datumbim-textSecondary">Desktop interaction and input control</p>
        </div>
        <button
          onClick={loadSessions}
          disabled={loading}
          className="text-[10px] px-2 py-1 bg-datumbim-border text-datumbim-text rounded hover:bg-datumbim-border/80 disabled:opacity-50"
        >
          Refresh Sessions
        </button>
      </div>
      <div className="flex-1 grid grid-cols-1 md:grid-cols-3 gap-3">
        <div className="bg-datumbim-surface border border-datumbim-border rounded p-3">
          <div className="text-[10px] font-semibold text-datumbim-textSecondary uppercase tracking-wider mb-2">Applications / Sessions</div>
          <div className="space-y-2">
            {sessions.map((session) => (
              <div
                key={session.id}
                className={`text-xs p-2 rounded border cursor-pointer ${
                  selectedSessionId === session.id ? 'border-datumbim-accent bg-datumbim-accent/10' : 'border-datumbim-border'
                }`}
                onClick={() => setSelectedSessionId(session.id)}
              >
                <div className="font-medium text-datumbim-text">{session.applicationId}</div>
                <div className="text-[10px] text-datumbim-textSecondary">{session.id}</div>
              </div>
            ))}
            {sessions.length === 0 && (
              <div className="text-xs text-datumbim-textSecondary text-center py-4">No sessions available</div>
            )}
          </div>
        </div>
        <div className="bg-datumbim-surface border border-datumbim-border rounded p-3">
          <div className="text-[10px] font-semibold text-datumbim-textSecondary uppercase tracking-wider mb-2">Action Console</div>
          <div className="space-y-2">
            <div>
              <label className="text-[10px] text-datumbim-textSecondary">Action Type</label>
              <select value={actionType} onChange={(e) => setActionType(e.target.value)} className="w-full mt-1 text-xs p-1 rounded border border-datumbim-border bg-datumbim-bg text-datumbim-text">
                <option value="mouse_move">Mouse Move</option>
                <option value="mouse_click">Mouse Click</option>
                <option value="mouse_double_click">Mouse Double Click</option>
                <option value="mouse_right_click">Mouse Right Click</option>
                <option value="mouse_drag">Mouse Drag</option>
                <option value="mouse_scroll">Mouse Scroll</option>
                <option value="keyboard_key">Keyboard Key</option>
                <option value="keyboard_type">Keyboard Type</option>
                <option value="keyboard_hotkey">Keyboard Hotkey</option>
                <option value="window_activate">Window Activate</option>
                <option value="window_minimize">Window Minimize</option>
                <option value="window_maximize">Window Maximize</option>
                <option value="window_restore">Window Restore</option>
                <option value="window_resize">Window Resize</option>
                <option value="window_move">Window Move</option>
                <option value="window_close">Window Close</option>
                <option value="application_launch">Application Launch</option>
                <option value="application_close">Application Close</option>
                <option value="application_focus">Application Focus</option>
              </select>
            </div>
            <div>
              <label className="text-[10px] text-datumbim-textSecondary">Parameters (JSON)</label>
              <textarea value={parameters} onChange={(e) => setParameters(e.target.value)} className="w-full mt-1 text-xs p-1 rounded border border-datumbim-border bg-datumbim-bg text-datumbim-text font-mono" rows={3} />
            </div>
            <div className="flex flex-wrap gap-2">
              <select value={riskLevel} onChange={(e) => setRiskLevel(e.target.value)} className="text-xs p-1 rounded border border-datumbim-border bg-datumbim-bg text-datumbim-text">
                <option value="low">Low Risk</option>
                <option value="medium">Medium Risk</option>
                <option value="high">High Risk</option>
                <option value="critical">Critical</option>
              </select>
              <label className="flex items-center gap-1 text-xs text-datumbim-text">
                <input type="checkbox" checked={approvalRequired} onChange={(e) => setApprovalRequired(e.target.checked)} />
                Approval Required
              </label>
              <label className="flex items-center gap-1 text-xs text-datumbim-text">
                <input type="checkbox" checked={dryRun} onChange={(e) => setDryRun(e.target.checked)} />
                Dry Run
              </label>
            </div>
            <button onClick={handleExecute} disabled={!selectedSessionId || loading} className="w-full text-xs px-2 py-1 bg-datumbim-accent text-white rounded hover:bg-datumbim-accent/80 disabled:opacity-50">
              {loading ? 'Executing...' : 'Execute Action'}
            </button>
          </div>
        </div>
        <div className="bg-datumbim-surface border border-datumbim-border rounded p-3">
          <div className="text-[10px] font-semibold text-datumbim-textSecondary uppercase tracking-wider mb-2">Execution Monitor</div>
          <div className="space-y-2">
            {actions.map((action) => (
              <div key={action.action_id} className="text-xs p-2 rounded border border-datumbim-border">
                <div className="flex items-center justify-between mb-1">
                  <span className="font-medium text-datumbim-text">{action.action_type}</span>
                  <span className={`text-[10px] px-1.5 py-0.5 rounded ${
                    action.status === 'completed' ? 'bg-green-500/10 text-green-400' :
                    action.status === 'dry_run' ? 'bg-blue-500/10 text-blue-400' :
                    action.status === 'approval_required' ? 'bg-yellow-500/10 text-yellow-400' :
                    'bg-red-500/10 text-red-400'
                  }`}>{action.status.toUpperCase()}</span>
                </div>
                <div className="text-[10px] text-datumbim-textSecondary">{action.application_id} • {new Date(action.timestamp).toLocaleString()}</div>
              </div>
            ))}
            {actions.length === 0 && (
              <div className="text-xs text-datumbim-textSecondary text-center py-4">No actions executed yet</div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
