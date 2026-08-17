'use client'

import React, { useState, useEffect, useCallback } from 'react'
import { useShellStore } from '@/store/shellStore'
import { apiClient } from '@/lib/apiClient'

interface Execution {
  execution_id: string
  status: string
  tool_id: string
  integration_id: string
  application_id?: string
  session_id?: string
  requested_by: string
  risk_level: string
  approval_required: boolean
  approval_state: string
  dry_run: boolean
  started_at?: string
  completed_at?: string
  duration?: number
  provider?: string
  tool?: string
  result?: any
  error?: string
  verification_state?: string
  observation_id?: string
  audit_id?: string
  metadata?: Record<string, any>
}

interface ToolInfo {
  tool_id: string
  name: string
  description: string
  category: string
  provider: string
  integration_id: string
  application_id?: string
  capabilities: string[]
  risk_level: string
  requires_approval: boolean
  requires_session: boolean
  requires_observation: boolean
  requires_verification: boolean
  timeout: number
  enabled: boolean
  availability: string
  execution_mode: string
}

export default function ExecutionCenter() {
  const { addNotification } = useShellStore()
  const [executions, setExecutions] = useState<Execution[]>([])
  const [tools, setTools] = useState<ToolInfo[]>([])
  const [loading, setLoading] = useState(false)
  const [selectedExecution, setSelectedExecution] = useState<Execution | null>(null)
  const [activeTab, setActiveTab] = useState<'executions' | 'tools'>('executions')
  const [filterStatus, setFilterStatus] = useState<string>('all')

  const loadExecutions = useCallback(async () => {
    setLoading(true)
    try {
      const res = await apiClient.get<{ executions: Execution[] }>('/execution/tools')
      if (res.error) throw new Error(res.error)
      setExecutions([])
    } catch (e) {
      addNotification({ type: 'error', message: 'Failed to load executions' })
    } finally {
      setLoading(false)
    }
  }, [addNotification])

  const loadTools = useCallback(async () => {
    setLoading(true)
    try {
      const res = await apiClient.get<{ tools: ToolInfo[] }>('/execution/tools')
      if (res.error) throw new Error(res.error)
      setTools(res.data?.tools ?? [])
    } catch (e) {
      addNotification({ type: 'error', message: 'Failed to load tools' })
    } finally {
      setLoading(false)
    }
  }, [addNotification])

  useEffect(() => {
    if (activeTab === 'executions') loadExecutions()
    else loadTools()
  }, [activeTab, loadExecutions, loadTools])

  const handleExecute = async (toolId: string) => {
    try {
      const req = {
        execution_id: `exec-${Date.now()}`,
        tool_id: toolId,
        integration_id: 'test',
        requested_by: 'user',
        parameters: {},
        risk_level: 'low',
        approval_required: false,
        approval_state: 'approved',
        dry_run: true,
        timeout: 30,
        created_at: new Date().toISOString(),
      }
      const res = await apiClient.post<Execution>('/execution/execute', req)
      if (res.error) throw new Error(res.error)
      addNotification({ type: 'success', message: `Executed ${toolId}` })
      loadExecutions()
    } catch (e) {
      addNotification({ type: 'error', message: `Failed to execute ${toolId}` })
    }
  }

  const handleCancel = async (executionId: string) => {
    try {
      const res = await apiClient.post(`/execution/${encodeURIComponent(executionId)}/cancel`, {})
      if (res.error) throw new Error(res.error)
      addNotification({ type: 'success', message: 'Execution cancelled' })
      loadExecutions()
    } catch (e) {
      addNotification({ type: 'error', message: 'Failed to cancel execution' })
    }
  }

  const statusColor = (status: string) => {
    switch (status) {
      case 'succeeded':
      case 'completed':
        return 'text-green-400'
      case 'failed':
      case 'verification_failed':
        return 'text-red-400'
      case 'running':
        return 'text-yellow-400'
      case 'queued':
      case 'waiting_approval':
        return 'text-blue-400'
      case 'cancelled':
      case 'timeout':
        return 'text-gray-400'
      case 'unavailable':
      case 'auth_required':
        return 'text-orange-400'
      default:
        return 'text-datumbim-textSecondary'
    }
  }

  const availabilityBadge = (availability: string) => {
    switch (availability) {
      case 'available':
      case 'connected':
        return 'bg-green-500/20 text-green-400'
      case 'unavailable':
      case 'not_installed':
        return 'bg-red-500/20 text-red-400'
      case 'auth_required':
      case 'not_configured':
        return 'bg-yellow-500/20 text-yellow-400'
      case 'mock':
      case 'simulated':
        return 'bg-gray-500/20 text-gray-400'
      default:
        return 'bg-gray-500/20 text-gray-400'
    }
  }

  const filteredExecutions = filterStatus === 'all' ? executions : executions.filter(e => e.status === filterStatus)

  return (
    <div className="h-full flex flex-col">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h2 className="text-sm font-semibold text-datumbim-text">Execution Center</h2>
          <p className="text-xs text-datumbim-textSecondary">Universal tool execution and runtime</p>
        </div>
        <div className="flex gap-2">
          <select
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value)}
            className="text-[10px] px-2 py-1 bg-datumbim-border text-datumbim-text rounded border border-datumbim-border"
          >
            <option value="all">All Status</option>
            <option value="queued">Queued</option>
            <option value="running">Running</option>
            <option value="succeeded">Succeeded</option>
            <option value="failed">Failed</option>
            <option value="waiting_approval">Waiting Approval</option>
            <option value="cancelled">Cancelled</option>
            <option value="unavailable">Unavailable</option>
            <option value="auth_required">Auth Required</option>
          </select>
          <button
            onClick={activeTab === 'executions' ? loadExecutions : loadTools}
            disabled={loading}
            className="text-[10px] px-2 py-1 bg-datumbim-border text-datumbim-text rounded hover:bg-datumbim-border/80 disabled:opacity-50"
          >
            Refresh
          </button>
        </div>
      </div>
      <div className="flex gap-2 mb-4">
        {(['executions', 'tools'] as const).map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`text-[10px] px-2 py-1 rounded capitalize ${
              activeTab === tab ? 'bg-datumbim-accent text-white' : 'bg-datumbim-border text-datumbim-text'
            }`}
          >
            {tab}
          </button>
        ))}
      </div>
      <div className="flex-1 grid grid-cols-1 md:grid-cols-3 gap-3">
        <div className="bg-datumbim-surface border border-datumbim-border rounded p-3">
          <div className="text-[10px] font-semibold text-datumbim-textSecondary uppercase tracking-wider mb-2">
            {activeTab === 'executions' ? 'Executions' : 'Tools'}
          </div>
          <div className="space-y-2 overflow-auto max-h-[500px]">
            {(activeTab === 'executions' ? filteredExecutions : tools).map((item: any) => (
              <div
                key={(item as any).execution_id || (item as any).tool_id}
                className={`text-xs p-2 rounded border cursor-pointer ${
                  (selectedExecution as any)?.execution_id === (item as any).execution_id || (activeTab === 'tools' && (selectedExecution as any)?.tool_id === (item as any).tool_id)
                    ? 'border-datumbim-accent bg-datumbim-accent/10'
                    : 'border-datumbim-border'
                }`}
                onClick={() => setSelectedExecution(item as Execution)}
              >
                <div className="font-medium text-datumbim-text">
                  {(item as any).tool_id || (item as any).name}
                </div>
                <div className={`text-[10px] ${statusColor((item as any).status || 'idle')}`}>
                  {((item as any).status || (item as any).execution_mode || 'idle').toUpperCase()}
                </div>
                <div className="text-[10px] text-datumbim-textSecondary">
                  {(item as any).integration_id || (item as any).provider || ''}
                </div>
                {activeTab === 'tools' && (
                  <div className={`text-[10px] mt-1 inline-block px-1 rounded ${availabilityBadge((item as any).availability)}`}>
                    {(item as any).availability?.toUpperCase() || 'UNKNOWN'}
                  </div>
                )}
              </div>
            ))}
            {(activeTab === 'executions' ? filteredExecutions : tools).length === 0 && (
              <div className="text-xs text-datumbim-textSecondary text-center py-4">
                No {activeTab} available
              </div>
            )}
          </div>
        </div>
        <div className="bg-datumbim-surface border border-datumbim-border rounded p-3">
          <div className="text-[10px] font-semibold text-datumbim-textSecondary uppercase tracking-wider mb-2">Details</div>
          {selectedExecution ? (
            <div className="space-y-2">
              <div className="text-xs text-datumbim-text">
                {(activeTab === 'executions' ? 'Execution ID' : 'Tool ID')}: {(selectedExecution as any).execution_id || (selectedExecution as any).tool_id}
              </div>
              <div className={`text-xs ${statusColor((selectedExecution as any).status || 'idle')}`}>
                Status: {((selectedExecution as any).status || 'idle').toUpperCase()}
              </div>
              {(selectedExecution as any).tool_id && (
                <div className="text-xs text-datumbim-textSecondary">
                  Tool: {(selectedExecution as any).tool_id}
                </div>
              )}
              <div className="text-xs text-datumbim-textSecondary">
                Integration: {(selectedExecution as any).integration_id || '-'}
              </div>
              <div className="text-xs text-datumbim-textSecondary">
                Requested By: {(selectedExecution as any).requested_by || '-'}
              </div>
              <div className="text-xs text-datumbim-textSecondary">
                Risk Level: {(selectedExecution as any).risk_level || '-'}
              </div>
              <div className="text-xs text-datumbim-textSecondary">
                Approval Required: {(selectedExecution as any).approval_required ? 'Yes' : 'No'}
              </div>
              {(selectedExecution as any).error && (
                <div className="text-xs text-red-400">
                  Error: {(selectedExecution as any).error}
                </div>
              )}
              {(selectedExecution as any).result && (
                <div className="text-xs text-datumbim-textSecondary">
                  Result: {JSON.stringify((selectedExecution as any).result).slice(0, 200)}
                </div>
              )}
            </div>
          ) : (
            <div className="text-xs text-datumbim-textSecondary text-center py-4">Select an item to view details</div>
          )}
        </div>
        <div className="bg-datumbim-surface border border-datumbim-border rounded p-3">
          <div className="text-[10px] font-semibold text-datumbim-textSecondary uppercase tracking-wider mb-2">Actions</div>
          {selectedExecution && activeTab === 'executions' ? (
            <div className="space-y-2">
              {(selectedExecution as any).status === 'running' && (
                <button
                  onClick={() => handleCancel((selectedExecution as any).execution_id)}
                  className="w-full text-xs px-2 py-1 bg-red-500/20 text-red-400 rounded hover:bg-red-500/30"
                >
                  Cancel
                </button>
              )}
              {['failed', 'timeout', 'verification_failed'].includes((selectedExecution as any).status) && (
                <button
                  onClick={() => addNotification({ type: 'info', message: 'Retry requires backend support' })}
                  className="w-full text-xs px-2 py-1 bg-datumbim-accent text-white rounded hover:bg-datumbim-accent/80"
                >
                  Retry
                </button>
              )}
            </div>
          ) : selectedExecution && activeTab === 'tools' ? (
            <div className="space-y-2">
              <button
                onClick={() => handleExecute((selectedExecution as any).tool_id)}
                className="w-full text-xs px-2 py-1 bg-datumbim-accent text-white rounded hover:bg-datumbim-accent/80"
              >
                Execute (Dry Run)
              </button>
            </div>
          ) : (
            <div className="text-xs text-datumbim-textSecondary text-center py-4">
              {activeTab === 'executions' ? 'Select an execution to manage' : 'Select a tool to execute'}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
