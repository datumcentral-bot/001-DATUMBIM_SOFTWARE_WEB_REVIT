'use client'

import React, { useState, useEffect, useCallback } from 'react'
import { useShellStore } from '@/store/shellStore'
import { apiClient } from '@/lib/apiClient'

interface AgentDefinition {
  agent_id: string
  name: string
  description: string
  version?: string
  provider: string
  model?: string
  system_policy: string
  tools: string[]
  allowed_integrations: string[]
  allowed_applications: string[]
  permissions: string[]
  approval_policy: string
  max_steps: number
  max_execution_time: number
  max_retries: number
  max_tool_calls: number
  enabled: boolean
  memory_policy: string
  observation_policy: string
  verification_policy: string
  failure_policy: string
  autonomy_level: string
}

interface AgentRun {
  run_id: string
  agent_id: string
  goal: string
  status: string
  session_id?: string
  application_id?: string
  created_at?: string
  started_at?: string
  completed_at?: string
  current_step: number
  max_steps: number
  steps: any[]
  result?: any
  error?: string
  verification_state?: string
  metadata?: Record<string, any>
}

export default function AgentControlCenter() {
  const { addNotification } = useShellStore()
  const [agents, setAgents] = useState<AgentDefinition[]>([])
  const [runs, setRuns] = useState<AgentRun[]>([])
  const [selectedAgent, setSelectedAgent] = useState<AgentDefinition | null>(null)
  const [selectedRun, setSelectedRun] = useState<AgentRun | null>(null)
  const [loading, setLoading] = useState(false)
  const [running, setRunning] = useState(false)
  const [activeTab, setActiveTab] = useState<'agents' | 'runs'>('agents')
  const [showCreate, setShowCreate] = useState(false)
  const [newAgent, setNewAgent] = useState({ agent_id: '', name: '', description: '', model: '', autonomy_level: 'level_2', approval_policy: 'required', max_steps: 10, failure_policy: 'replan' })
  const [runGoal, setRunGoal] = useState('')

  const loadAgents = useCallback(async () => {
    setLoading(true)
    try {
      const res = await apiClient.get<{ agents: AgentDefinition[] }>('/agents')
      if (res.error) throw new Error(res.error)
      setAgents(res.data?.agents ?? [])
    } catch (e) {
      addNotification({ type: 'error', message: 'Failed to load agents' })
    } finally {
      setLoading(false)
    }
  }, [addNotification])

  const loadRuns = useCallback(async () => {
    setLoading(true)
    try {
      const res = await apiClient.get<{ runs: AgentRun[] }>('/agents/runs')
      if (res.error) throw new Error(res.error)
      setRuns(res.data?.runs ?? [])
    } catch (e) {
      addNotification({ type: 'error', message: 'Failed to load runs' })
    } finally {
      setLoading(false)
    }
  }, [addNotification])

  useEffect(() => {
    if (activeTab === 'agents') loadAgents()
    else loadRuns()
  }, [activeTab, loadAgents, loadRuns])

  const handleCreateAgent = async () => {
    if (!newAgent.agent_id || !newAgent.name) {
      addNotification({ type: 'error', message: 'agent_id and name are required' })
      return
    }
    try {
      const agent: AgentDefinition = {
        agent_id: newAgent.agent_id,
        name: newAgent.name,
        description: newAgent.description,
        provider: 'datumbim',
        model: newAgent.model,
        system_policy: 'safe_default',
        tools: [],
        allowed_integrations: [],
        allowed_applications: [],
        permissions: [],
        approval_policy: newAgent.approval_policy,
        max_steps: newAgent.max_steps,
        max_execution_time: 300,
        max_retries: 2,
        max_tool_calls: 20,
        enabled: true,
        memory_policy: 'run_scoped',
        observation_policy: 'after_relevant_actions',
        verification_policy: 'explicit',
        failure_policy: newAgent.failure_policy as any,
        autonomy_level: newAgent.autonomy_level as any,
      }
      const res = await apiClient.post<AgentDefinition>('/agents', agent)
      if (res.error) throw new Error(res.error)
      addNotification({ type: 'success', message: `Agent ${newAgent.agent_id} created` })
      setShowCreate(false)
      setNewAgent({ agent_id: '', name: '', description: '', model: '', autonomy_level: 'level_2', approval_policy: 'required', max_steps: 10, failure_policy: 'replan' })
      loadAgents()
    } catch (e) {
      addNotification({ type: 'error', message: 'Failed to create agent' })
    }
  }

  const handleRunAgent = async (agentId: string) => {
    if (!runGoal.trim()) {
      addNotification({ type: 'error', message: 'Goal is required' })
      return
    }
    setRunning(true)
    try {
      const res = await apiClient.post<AgentRun>(`/agents/${encodeURIComponent(agentId)}/run`, { goal: runGoal, dry_run: true })
      if (res.error) throw new Error(res.error)
      addNotification({ type: 'success', message: `Agent run started` })
      setRunGoal('')
      loadRuns()
    } catch (e) {
      addNotification({ type: 'error', message: 'Failed to start agent run' })
    } finally {
      setRunning(false)
    }
  }

  const handleApprove = async (runId: string, stepId: string) => {
    try {
      const res = await apiClient.post(`/agents/runs/${encodeURIComponent(runId)}/approve`, { step_id: stepId })
      if (res.error) throw new Error(res.error)
      addNotification({ type: 'success', message: 'Step approved' })
      loadRuns()
    } catch (e) {
      addNotification({ type: 'error', message: 'Failed to approve step' })
    }
  }

  const handleReject = async (runId: string, stepId: string) => {
    try {
      const res = await apiClient.post(`/agents/runs/${encodeURIComponent(runId)}/reject`, { step_id: stepId })
      if (res.error) throw new Error(res.error)
      addNotification({ type: 'success', message: 'Step rejected' })
      loadRuns()
    } catch (e) {
      addNotification({ type: 'error', message: 'Failed to reject step' })
    }
  }

  const handleCancel = async (runId: string) => {
    try {
      const res = await apiClient.post(`/agents/runs/${encodeURIComponent(runId)}/cancel`, {})
      if (res.error) throw new Error(res.error)
      addNotification({ type: 'success', message: 'Run cancelled' })
      loadRuns()
    } catch (e) {
      addNotification({ type: 'error', message: 'Failed to cancel run' })
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
      case 'planning':
      case 'observing':
      case 'verifying':
      case 'replanning':
        return 'text-yellow-400'
      case 'queued':
      case 'waiting_approval':
        return 'text-blue-400'
      case 'cancelled':
      case 'timeout':
      case 'max_steps_reached':
        return 'text-gray-400'
      case 'unavailable':
      case 'auth_required':
        return 'text-orange-400'
      default:
        return 'text-datumbim-textSecondary'
    }
  }

  const autonomyLabel = (level: string) => {
    switch (level) {
      case 'level_0': return 'L0 Read Only'
      case 'level_1': return 'L1 Suggest'
      case 'level_2': return 'L2 Approval Required'
      case 'level_3': return 'L3 Supervised'
      case 'level_4': return 'L4 Autonomous'
      default: return level
    }
  }

  return (
    <div className="h-full flex flex-col">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h2 className="text-sm font-semibold text-datumbim-text">Agent Control Center</h2>
          <p className="text-xs text-datumbim-textSecondary">AI agent runtime and orchestration</p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={() => setShowCreate(true)}
            disabled={loading || running}
            className="text-[10px] px-2 py-1 bg-datumbim-accent text-white rounded hover:bg-datumbim-accent/80 disabled:opacity-50"
          >
            New Agent
          </button>
          <button
            onClick={activeTab === 'agents' ? loadAgents : loadRuns}
            disabled={loading}
            className="text-[10px] px-2 py-1 bg-datumbim-border text-datumbim-text rounded hover:bg-datumbim-border/80 disabled:opacity-50"
          >
            Refresh
          </button>
        </div>
      </div>
      {showCreate && (
        <div className="mb-4 p-3 bg-datumbim-surface border border-datumbim-border rounded">
          <div className="text-xs font-semibold text-datumbim-text mb-2">Create Agent</div>
          <div className="grid grid-cols-2 gap-2">
            <input
              type="text"
              placeholder="Agent ID"
              value={newAgent.agent_id}
              onChange={(e) => setNewAgent({ ...newAgent, agent_id: e.target.value })}
              className="text-xs px-2 py-1 bg-datumbim-border text-datumbim-text rounded border border-datumbim-border"
            />
            <input
              type="text"
              placeholder="Name"
              value={newAgent.name}
              onChange={(e) => setNewAgent({ ...newAgent, name: e.target.value })}
              className="text-xs px-2 py-1 bg-datumbim-border text-datumbim-text rounded border border-datumbim-border"
            />
            <input
              type="text"
              placeholder="Description"
              value={newAgent.description}
              onChange={(e) => setNewAgent({ ...newAgent, description: e.target.value })}
              className="text-xs px-2 py-1 bg-datumbim-border text-datumbim-text rounded border border-datumbim-border col-span-2"
            />
            <input
              type="text"
              placeholder="Model (optional)"
              value={newAgent.model}
              onChange={(e) => setNewAgent({ ...newAgent, model: e.target.value })}
              className="text-xs px-2 py-1 bg-datumbim-border text-datumbim-text rounded border border-datumbim-border"
            />
            <select
              value={newAgent.autonomy_level}
              onChange={(e) => setNewAgent({ ...newAgent, autonomy_level: e.target.value })}
              className="text-xs px-2 py-1 bg-datumbim-border text-datumbim-text rounded border border-datumbim-border"
            >
              <option value="level_0">Level 0 - Read Only</option>
              <option value="level_1">Level 1 - Suggest</option>
              <option value="level_2">Level 2 - Approval Required</option>
              <option value="level_3">Level 3 - Supervised</option>
              <option value="level_4">Level 4 - Autonomous</option>
            </select>
            <select
              value={newAgent.failure_policy}
              onChange={(e) => setNewAgent({ ...newAgent, failure_policy: e.target.value })}
              className="text-xs px-2 py-1 bg-datumbim-border text-datumbim-text rounded border border-datumbim-border"
            >
              <option value="fail_fast">Fail Fast</option>
              <option value="retry">Retry</option>
              <option value="replan">Replan</option>
              <option value="fallback_tool">Fallback Tool</option>
              <option value="ask_user">Ask User</option>
            </select>
            <input
              type="number"
              placeholder="Max Steps"
              value={newAgent.max_steps}
              onChange={(e) => setNewAgent({ ...newAgent, max_steps: parseInt(e.target.value) || 10 })}
              className="text-xs px-2 py-1 bg-datumbim-border text-datumbim-text rounded border border-datumbim-border"
            />
          </div>
          <div className="flex gap-2 mt-2">
            <button
              onClick={handleCreateAgent}
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
        {(['agents', 'runs'] as const).map((tab) => (
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
            {activeTab === 'agents' ? 'Agents' : 'Runs'}
          </div>
          <div className="space-y-2 overflow-auto max-h-[500px]">
            {(activeTab === 'agents' ? agents : runs).map((item: any) => (
              <div
                key={(item as any).agent_id || (item as any).run_id}
                className={`text-xs p-2 rounded border cursor-pointer ${
                  (selectedAgent as any)?.agent_id === (item as any).agent_id || (selectedRun as any)?.run_id === (item as any).run_id
                    ? 'border-datumbim-accent bg-datumbim-accent/10'
                    : 'border-datumbim-border'
                }`}
                onClick={() => activeTab === 'agents' ? setSelectedAgent(item as AgentDefinition) : setSelectedRun(item as AgentRun)}
              >
                <div className="font-medium text-datumbim-text">
                  {(item as any).name || (item as any).goal}
                </div>
                <div className={`text-[10px] ${statusColor((item as any).status || 'idle')}`}>
                  {((item as any).status || (item as any).autonomy_level || 'idle').toUpperCase()}
                </div>
                <div className="text-[10px] text-datumbim-textSecondary">
                  {(item as any).agent_id || (item as any).run_id || ''}
                </div>
              </div>
            ))}
            {(activeTab === 'agents' ? agents : runs).length === 0 && (
              <div className="text-xs text-datumbim-textSecondary text-center py-4">
                No {activeTab} available
              </div>
            )}
          </div>
        </div>
        <div className="bg-datumbim-surface border border-datumbim-border rounded p-3">
          <div className="text-[10px] font-semibold text-datumbim-textSecondary uppercase tracking-wider mb-2">Details</div>
          {activeTab === 'agents' && selectedAgent ? (
            <div className="space-y-2">
              <div className="text-xs text-datumbim-text">Name: {selectedAgent.name}</div>
              <div className="text-xs text-datumbim-textSecondary">ID: {selectedAgent.agent_id}</div>
              <div className="text-xs text-datumbim-textSecondary">Provider: {selectedAgent.provider}</div>
              <div className="text-xs text-datumbim-textSecondary">Model: {selectedAgent.model || '-'}</div>
              <div className="text-xs text-datumbim-textSecondary">Autonomy: {autonomyLabel(selectedAgent.autonomy_level)}</div>
              <div className="text-xs text-datumbim-textSecondary">Approval: {selectedAgent.approval_policy}</div>
              <div className="text-xs text-datumbim-textSecondary">Max Steps: {selectedAgent.max_steps}</div>
              <div className="text-xs text-datumbim-textSecondary">Failure Policy: {selectedAgent.failure_policy}</div>
              <div className="text-xs text-datumbim-textSecondary">Enabled: {selectedAgent.enabled ? 'Yes' : 'No'}</div>
              <div className="text-xs text-datumbim-textSecondary">Tools: {selectedAgent.tools.length}</div>
            </div>
          ) : selectedRun ? (
            <div className="space-y-2">
              <div className="text-xs text-datumbim-text">Goal: {selectedRun.goal}</div>
              <div className={`text-xs ${statusColor(selectedRun.status)}`}>Status: {selectedRun.status.toUpperCase()}</div>
              <div className="text-xs text-datumbim-textSecondary">Run ID: {selectedRun.run_id}</div>
              <div className="text-xs text-datumbim-textSecondary">Agent: {selectedRun.agent_id}</div>
              <div className="text-xs text-datumbim-textSecondary">Step: {selectedRun.current_step} / {selectedRun.max_steps}</div>
              {selectedRun.error && <div className="text-xs text-red-400">Error: {selectedRun.error}</div>}
              {selectedRun.steps.length > 0 && (
                <div className="space-y-1">
                  <div className="text-[10px] font-semibold text-datumbim-textSecondary uppercase">Steps</div>
                  {selectedRun.steps.map((step: any, idx: number) => (
                    <div key={idx} className="text-[10px] p-1 rounded border border-datumbim-border">
                      <span className="text-datumbim-text">Step {idx + 1}:</span> {step.tool_id || step.step_id} - {step.status}
                    </div>
                  ))}
                </div>
              )}
            </div>
          ) : (
            <div className="text-xs text-datumbim-textSecondary text-center py-4">Select an item to view details</div>
          )}
        </div>
        <div className="bg-datumbim-surface border border-datumbim-border rounded p-3">
          <div className="text-[10px] font-semibold text-datumbim-textSecondary uppercase tracking-wider mb-2">Actions</div>
          {activeTab === 'agents' && selectedAgent ? (
            <div className="space-y-2">
              <input
                type="text"
                placeholder="Enter goal..."
                value={runGoal}
                onChange={(e) => setRunGoal(e.target.value)}
                className="w-full text-xs px-2 py-1 bg-datumbim-border text-datumbim-text rounded border border-datumbim-border"
              />
              <button
                onClick={() => handleRunAgent(selectedAgent.agent_id)}
                disabled={running || !runGoal.trim()}
                className="w-full text-xs px-2 py-1 bg-datumbim-accent text-white rounded hover:bg-datumbim-accent/80 disabled:opacity-50"
              >
                {running ? 'Running...' : 'Run Agent'}
              </button>
            </div>
          ) : selectedRun ? (
            <div className="space-y-2">
              {selectedRun.status === 'waiting_approval' && selectedRun.steps.length > 0 && (
                <div className="space-y-2">
                  <button
                    onClick={() => handleApprove(selectedRun.run_id, selectedRun.steps[selectedRun.steps.length - 1].step_id)}
                    disabled={running}
                    className="w-full text-xs px-2 py-1 bg-green-500/20 text-green-400 rounded hover:bg-green-500/30 disabled:opacity-50"
                  >
                    Approve
                  </button>
                  <button
                    onClick={() => handleReject(selectedRun.run_id, selectedRun.steps[selectedRun.steps.length - 1].step_id)}
                    disabled={running}
                    className="w-full text-xs px-2 py-1 bg-red-500/20 text-red-400 rounded hover:bg-red-500/30 disabled:opacity-50"
                  >
                    Reject
                  </button>
                </div>
              )}
              {(selectedRun.status === 'running' || selectedRun.status === 'planning') && (
                <button
                  onClick={() => handleCancel(selectedRun.run_id)}
                  disabled={running}
                  className="w-full text-xs px-2 py-1 bg-red-500/20 text-red-400 rounded hover:bg-red-500/30 disabled:opacity-50"
                >
                  Cancel
                </button>
              )}
            </div>
          ) : (
            <div className="text-xs text-datumbim-textSecondary text-center py-4">
              {activeTab === 'agents' ? 'Select an agent to run' : 'Select a run to manage'}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
