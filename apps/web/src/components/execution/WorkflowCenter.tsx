'use client'

import React, { useState, useEffect, useCallback } from 'react'
import { useShellStore } from '@/store/shellStore'
import { apiClient } from '@/lib/apiClient'

interface Workflow {
  workflow_id: string
  name: string
  description: string
  version?: string
  inputs: Record<string, any>
  steps: any[]
  conditions: Record<string, any>
  outputs: Record<string, any>
  risk_level: string
  approval_policy: string
  enabled: boolean
  created_at?: string
  updated_at?: string
}

interface WorkflowExecution {
  execution_id: string
  workflow_id: string
  status: string
  current_step: number
  inputs: Record<string, any>
  outputs: Record<string, any>
  steps: any[]
  started_at?: string
  completed_at?: string
  duration?: number
  error?: string
  metadata: Record<string, any>
}

export default function WorkflowCenter() {
  const { addNotification } = useShellStore()
  const [workflows, setWorkflows] = useState<Workflow[]>([])
  const [executions, setExecutions] = useState<WorkflowExecution[]>([])
  const [selectedWorkflow, setSelectedWorkflow] = useState<Workflow | null>(null)
  const [loading, setLoading] = useState(false)
  const [running, setRunning] = useState(false)
  const [activeTab, setActiveTab] = useState<'workflows' | 'executions'>('workflows')
  const [showCreate, setShowCreate] = useState(false)
  const [newWorkflow, setNewWorkflow] = useState({ workflow_id: '', name: '', description: '', risk_level: 'low', approval_policy: 'none' })

  const loadWorkflows = useCallback(async () => {
    setLoading(true)
    try {
      const res = await apiClient.get<{ workflows: Workflow[] }>('/workflows')
      if (res.error) throw new Error(res.error)
      setWorkflows(res.data?.workflows ?? [])
    } catch (e) {
      addNotification({ type: 'error', message: 'Failed to load workflows' })
    } finally {
      setLoading(false)
    }
  }, [addNotification])

  const loadExecutions = useCallback(async () => {
    setLoading(true)
    try {
      const res = await apiClient.get<{ executions: WorkflowExecution[] }>('/execution/tools')
      if (res.error) throw new Error(res.error)
      setExecutions([])
    } catch (e) {
      addNotification({ type: 'error', message: 'Failed to load executions' })
    } finally {
      setLoading(false)
    }
  }, [addNotification])

  useEffect(() => {
    if (activeTab === 'workflows') loadWorkflows()
    else loadExecutions()
  }, [activeTab, loadWorkflows, loadExecutions])

  const handleCreateWorkflow = async () => {
    if (!newWorkflow.workflow_id || !newWorkflow.name) {
      addNotification({ type: 'error', message: 'workflow_id and name are required' })
      return
    }
    try {
      const workflow: Workflow = {
        workflow_id: newWorkflow.workflow_id,
        name: newWorkflow.name,
        description: newWorkflow.description,
        version: '1.0.0',
        inputs: {},
        steps: [],
        conditions: {},
        outputs: {},
        risk_level: newWorkflow.risk_level,
        approval_policy: newWorkflow.approval_policy,
        enabled: true,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      }
      const res = await apiClient.post<Workflow>('/workflows', workflow)
      if (res.error) throw new Error(res.error)
      addNotification({ type: 'success', message: `Workflow ${newWorkflow.workflow_id} created` })
      setShowCreate(false)
      setNewWorkflow({ workflow_id: '', name: '', description: '', risk_level: 'low', approval_policy: 'none' })
      loadWorkflows()
    } catch (e) {
      addNotification({ type: 'error', message: 'Failed to create workflow' })
    }
  }

  const handleRunWorkflow = async (workflowId: string) => {
    setRunning(true)
    try {
      const res = await apiClient.post<WorkflowExecution>(`/workflows/${encodeURIComponent(workflowId)}/run`, { inputs: {}, dry_run: true })
      if (res.error) throw new Error(res.error)
      addNotification({ type: 'success', message: `Workflow ${workflowId} started` })
      loadWorkflows()
    } catch (e) {
      addNotification({ type: 'error', message: `Failed to run workflow ${workflowId}` })
    } finally {
      setRunning(false)
    }
  }

  const handleCancelWorkflow = async (workflowId: string) => {
    try {
      const res = await apiClient.post(`/workflows/${encodeURIComponent(workflowId)}/cancel`, {})
      if (res.error) throw new Error(res.error)
      addNotification({ type: 'success', message: `Workflow ${workflowId} cancelled` })
      loadWorkflows()
    } catch (e) {
      addNotification({ type: 'error', message: `Failed to cancel workflow ${workflowId}` })
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

  return (
    <div className="h-full flex flex-col">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h2 className="text-sm font-semibold text-datumbim-text">Workflow Center</h2>
          <p className="text-xs text-datumbim-textSecondary">Composable execution workflows</p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={() => setShowCreate(true)}
            disabled={loading || running}
            className="text-[10px] px-2 py-1 bg-datumbim-accent text-white rounded hover:bg-datumbim-accent/80 disabled:opacity-50"
          >
            New Workflow
          </button>
          <button
            onClick={activeTab === 'workflows' ? loadWorkflows : loadExecutions}
            disabled={loading}
            className="text-[10px] px-2 py-1 bg-datumbim-border text-datumbim-text rounded hover:bg-datumbim-border/80 disabled:opacity-50"
          >
            Refresh
          </button>
        </div>
      </div>
      {showCreate && (
        <div className="mb-4 p-3 bg-datumbim-surface border border-datumbim-border rounded">
          <div className="text-xs font-semibold text-datumbim-text mb-2">Create Workflow</div>
          <div className="grid grid-cols-2 gap-2">
            <input
              type="text"
              placeholder="Workflow ID"
              value={newWorkflow.workflow_id}
              onChange={(e) => setNewWorkflow({ ...newWorkflow, workflow_id: e.target.value })}
              className="text-xs px-2 py-1 bg-datumbim-border text-datumbim-text rounded border border-datumbim-border"
            />
            <input
              type="text"
              placeholder="Name"
              value={newWorkflow.name}
              onChange={(e) => setNewWorkflow({ ...newWorkflow, name: e.target.value })}
              className="text-xs px-2 py-1 bg-datumbim-border text-datumbim-text rounded border border-datumbim-border"
            />
            <input
              type="text"
              placeholder="Description"
              value={newWorkflow.description}
              onChange={(e) => setNewWorkflow({ ...newWorkflow, description: e.target.value })}
              className="text-xs px-2 py-1 bg-datumbim-border text-datumbim-text rounded border border-datumbim-border col-span-2"
            />
            <select
              value={newWorkflow.risk_level}
              onChange={(e) => setNewWorkflow({ ...newWorkflow, risk_level: e.target.value })}
              className="text-xs px-2 py-1 bg-datumbim-border text-datumbim-text rounded border border-datumbim-border"
            >
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
              <option value="critical">Critical</option>
            </select>
            <select
              value={newWorkflow.approval_policy}
              onChange={(e) => setNewWorkflow({ ...newWorkflow, approval_policy: e.target.value })}
              className="text-xs px-2 py-1 bg-datumbim-border text-datumbim-text rounded border border-datumbim-border"
            >
              <option value="none">None</option>
              <option value="required">Required</option>
              <option value="auto">Auto</option>
            </select>
          </div>
          <div className="flex gap-2 mt-2">
            <button
              onClick={handleCreateWorkflow}
              disabled={running}
              className="text-[10px] px-2 py-1 bg-datumbim-accent text-white rounded hover:bg-datumbim-accent/80 disabled:opacity-50"
            >
              Create
            </button>
            <button
              onClick={() => setShowCreate(false)}
              disabled={running}
              className="text-[10px] px-2 py-1 bg-datumbim-border text-datumbim-text rounded hover:bg-datumbim-border/80 disabled:opacity-50"
            >
              Cancel
            </button>
          </div>
        </div>
      )}
      <div className="flex gap-2 mb-4">
        {(['workflows', 'executions'] as const).map((tab) => (
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
            {activeTab === 'workflows' ? 'Workflows' : 'Executions'}
          </div>
          <div className="space-y-2 overflow-auto max-h-[500px]">
            {(activeTab === 'workflows' ? workflows : executions).map((item: any) => (
              <div
                key={(item as any).workflow_id || (item as any).execution_id}
                className={`text-xs p-2 rounded border cursor-pointer ${
                  (selectedWorkflow as any)?.workflow_id === (item as any).workflow_id || (activeTab === 'executions' && (selectedWorkflow as any)?.execution_id === (item as any).execution_id)
                    ? 'border-datumbim-accent bg-datumbim-accent/10'
                    : 'border-datumbim-border'
                }`}
                onClick={() => setSelectedWorkflow(item as Workflow)}
              >
                <div className="font-medium text-datumbim-text">
                  {(item as any).name || (item as any).workflow_id}
                </div>
                <div className={`text-[10px] ${statusColor((item as any).status || 'idle')}`}>
                  {((item as any).status || (item as any).approval_policy || 'idle').toUpperCase()}
                </div>
                <div className="text-[10px] text-datumbim-textSecondary">
                  {(item as any).workflow_id || (item as any).execution_id}
                </div>
              </div>
            ))}
            {(activeTab === 'workflows' ? workflows : executions).length === 0 && (
              <div className="text-xs text-datumbim-textSecondary text-center py-4">
                No {activeTab} available
              </div>
            )}
          </div>
        </div>
        <div className="bg-datumbim-surface border border-datumbim-border rounded p-3">
          <div className="text-[10px] font-semibold text-datumbim-textSecondary uppercase tracking-wider mb-2">Details</div>
          {selectedWorkflow ? (
            <div className="space-y-2">
              <div className="text-xs text-datumbim-text">
                {(activeTab === 'workflows' ? 'Workflow' : 'Execution')} ID: {(selectedWorkflow as any).workflow_id || (selectedWorkflow as any).execution_id}
              </div>
              <div className="text-xs text-datumbim-text">
                Name: {(selectedWorkflow as any).name}
              </div>
              <div className={`text-xs ${statusColor((selectedWorkflow as any).status || 'idle')}`}>
                Status: {((selectedWorkflow as any).status || 'idle').toUpperCase()}
              </div>
              <div className="text-xs text-datumbim-textSecondary">
                Risk Level: {(selectedWorkflow as any).risk_level || '-'}
              </div>
              <div className="text-xs text-datumbim-textSecondary">
                Approval Policy: {(selectedWorkflow as any).approval_policy || '-'}
              </div>
              <div className="text-xs text-datumbim-textSecondary">
                Enabled: {(selectedWorkflow as any).enabled ? 'Yes' : 'No'}
              </div>
              {(selectedWorkflow as any).steps && (selectedWorkflow as any).steps.length > 0 && (
                <div className="space-y-1">
                  <div className="text-[10px] font-semibold text-datumbim-textSecondary uppercase">Steps</div>
                  {(selectedWorkflow as any).steps.map((step: any, idx: number) => (
                    <div key={idx} className="text-[10px] p-1 rounded border border-datumbim-border">
                      <span className="text-datumbim-text">Step {idx + 1}:</span> {step.tool_id || step.action_type || JSON.stringify(step)}
                    </div>
                  ))}
                </div>
              )}
              {(selectedWorkflow as any).error && (
                <div className="text-xs text-red-400">
                  Error: {(selectedWorkflow as any).error}
                </div>
              )}
            </div>
          ) : (
            <div className="text-xs text-datumbim-textSecondary text-center py-4">Select a workflow to view details</div>
          )}
        </div>
        <div className="bg-datumbim-surface border border-datumbim-border rounded p-3">
          <div className="text-[10px] font-semibold text-datumbim-textSecondary uppercase tracking-wider mb-2">Actions</div>
          {selectedWorkflow && activeTab === 'workflows' ? (
            <div className="space-y-2">
              <button
                onClick={() => handleRunWorkflow((selectedWorkflow as any).workflow_id)}
                disabled={running || !(selectedWorkflow as any).enabled}
                className="w-full text-xs px-2 py-1 bg-datumbim-accent text-white rounded hover:bg-datumbim-accent/80 disabled:opacity-50"
              >
                {running ? 'Running...' : 'Run Workflow'}
              </button>
              <button
                onClick={() => handleCancelWorkflow((selectedWorkflow as any).workflow_id)}
                disabled={running}
                className="w-full text-xs px-2 py-1 bg-red-500/20 text-red-400 rounded hover:bg-red-500/30 disabled:opacity-50"
              >
                Cancel
              </button>
            </div>
          ) : (
            <div className="text-xs text-datumbim-textSecondary text-center py-4">
              {activeTab === 'workflows' ? 'Select a workflow to manage' : 'No actions available'}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
