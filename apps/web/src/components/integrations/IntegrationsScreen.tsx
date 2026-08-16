'use client'

import React, { useState, useEffect, useCallback } from 'react'
import { useShellStore } from '@/store/shellStore'
import { apiClient } from '@/lib/apiClient'

interface Integration {
  integration_id: string
  name: string
  description: string
  integration_type: string
  status: string
  version: string | null
  installed_path: string | null
  executable: string | null
  capabilities: { capability_id: string; name: string; description: string; category: string; available: boolean }[]
  metadata: Record<string, string>
  error: string | null
}

interface Tool {
  tool_id: string
  name: string
  description: string
  provider: string
  capabilities: string[]
  risk_level: string
  approval_required: boolean
  available: boolean
}

interface Workflow {
  workflow_id: string
  name: string
  description: string
  integration_id: string
  trigger: string
  execution_state: string
  risk_level: string
}

export default function IntegrationsScreen() {
  const { addNotification } = useShellStore()
  const [integrations, setIntegrations] = useState<Integration[]>([])
  const [tools, setTools] = useState<Tool[]>([])
  const [workflows, setWorkflows] = useState<Workflow[]>([])
  const [loading, setLoading] = useState(false)
  const [selectedIntegration, setSelectedIntegration] = useState<Integration | null>(null)
  const [activeTab, setActiveTab] = useState<'integrations' | 'tools' | 'workflows'>('integrations')

  const loadIntegrations = useCallback(async () => {
    setLoading(true)
    try {
      const res = await apiClient.get<{ integrations: Integration[] }>('/integrations')
      if (res.error) throw new Error(res.error)
      setIntegrations(res.data?.integrations ?? [])
    } catch (e) {
      addNotification({ type: 'error', message: 'Failed to load integrations' })
    } finally {
      setLoading(false)
    }
  }, [addNotification])

  const loadTools = useCallback(async () => {
    setLoading(true)
    try {
      const res = await apiClient.get<{ tools: Tool[] }>('/integrations/tools')
      if (res.error) throw new Error(res.error)
      setTools(res.data?.tools ?? [])
    } catch (e) {
      addNotification({ type: 'error', message: 'Failed to load tools' })
    } finally {
      setLoading(false)
    }
  }, [addNotification])

  const loadWorkflows = useCallback(async () => {
    setLoading(true)
    try {
      const res = await apiClient.get<{ workflows: Workflow[] }>('/integrations/workflows')
      if (res.error) throw new Error(res.error)
      setWorkflows(res.data?.workflows ?? [])
    } catch (e) {
      addNotification({ type: 'error', message: 'Failed to load workflows' })
    } finally {
      setLoading(false)
    }
  }, [addNotification])

  useEffect(() => {
    if (activeTab === 'integrations') loadIntegrations()
    else if (activeTab === 'tools') loadTools()
    else if (activeTab === 'workflows') loadWorkflows()
  }, [activeTab, loadIntegrations, loadTools, loadWorkflows])

  const handleConnect = async (integrationId: string) => {
    try {
      const res = await apiClient.post(`/integrations/${encodeURIComponent(integrationId)}/connect`, {})
      if (res.error) throw new Error(res.error)
      addNotification({ type: 'success', message: `Connected to ${integrationId}` })
      loadIntegrations()
    } catch (e) {
      addNotification({ type: 'error', message: `Failed to connect to ${integrationId}` })
    }
  }

  const handleDisconnect = async (integrationId: string) => {
    try {
      const res = await apiClient.post(`/integrations/${encodeURIComponent(integrationId)}/disconnect`, {})
      if (res.error) throw new Error(res.error)
      addNotification({ type: 'success', message: `Disconnected from ${integrationId}` })
      loadIntegrations()
    } catch (e) {
      addNotification({ type: 'error', message: `Failed to disconnect from ${integrationId}` })
    }
  }

  const statusColor = (status: string) => {
    switch (status) {
      case 'connected':
        return 'text-green-400'
      case 'ready':
        return 'text-green-400'
      case 'available':
        return 'text-yellow-400'
      case 'not_installed':
        return 'text-red-400'
      case 'not_configured':
        return 'text-orange-400'
      case 'auth_required':
        return 'text-yellow-400'
      case 'error':
        return 'text-red-400'
      case 'mock':
        return 'text-gray-400'
      default:
        return 'text-datumbim-textSecondary'
    }
  }

  return (
    <div className="h-full flex flex-col">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h2 className="text-sm font-semibold text-datumbim-text">Integrations</h2>
          <p className="text-xs text-datumbim-textSecondary">Universal application, API, and automation fabric</p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={loadIntegrations}
            disabled={loading}
            className="text-[10px] px-2 py-1 bg-datumbim-border text-datumbim-text rounded hover:bg-datumbim-border/80 disabled:opacity-50"
          >
            Refresh
          </button>
        </div>
      </div>
      <div className="flex gap-2 mb-4">
        {(['integrations', 'tools', 'workflows'] as const).map((tab) => (
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
            {activeTab === 'integrations' ? 'Integrations' : activeTab === 'tools' ? 'Tools' : 'Workflows'}
          </div>
          <div className="space-y-2 overflow-auto max-h-[500px]">
            {(activeTab === 'integrations' ? integrations : activeTab === 'tools' ? tools : workflows).map((item: any) => (
              <div
                key={(item as any).integration_id || (item as any).tool_id || (item as any).workflow_id}
                className={`text-xs p-2 rounded border cursor-pointer ${
                  (selectedIntegration as any)?.integration_id === (item as any).integration_id || (activeTab === 'tools' && (selectedIntegration as any)?.integration_id === (item as any).provider)
                    ? 'border-datumbim-accent bg-datumbim-accent/10'
                    : 'border-datumbim-border'
                }`}
                onClick={() => setSelectedIntegration(item as Integration)}
              >
                <div className="font-medium text-datumbim-text">
                  {(item as any).name || (item as any).tool_id || (item as any).workflow_id}
                </div>
                <div className={`text-[10px] ${statusColor(item.status || (item as any).execution_state || 'idle')}`}>
                  {(item.status || (item as any).execution_state || 'idle').toUpperCase()}
                </div>
                <div className="text-[10px] text-datumbim-textSecondary">
                  {(item as any).integration_type || (item as any).provider || ''}
                </div>
              </div>
            ))}
            {(activeTab === 'integrations' ? integrations : activeTab === 'tools' ? tools : workflows).length === 0 && (
              <div className="text-xs text-datumbim-textSecondary text-center py-4">
                No {activeTab} available
              </div>
            )}
          </div>
        </div>
        <div className="bg-datumbim-surface border border-datumbim-border rounded p-3">
          <div className="text-[10px] font-semibold text-datumbim-textSecondary uppercase tracking-wider mb-2">Details</div>
          {selectedIntegration ? (
            <div className="space-y-2">
              <div className="text-xs text-datumbim-text">
                Name: {(selectedIntegration as any).name || (selectedIntegration as any).tool_id || (selectedIntegration as any).workflow_id}
              </div>
              <div className={`text-xs ${statusColor((selectedIntegration as any).status || (selectedIntegration as any).execution_state || 'idle')}`}>
                Status: {((selectedIntegration as any).status || (selectedIntegration as any).execution_state || 'idle').toUpperCase()}
              </div>
              <div className="text-xs text-datumbim-textSecondary">
                Type: {(selectedIntegration as any).integration_type || (selectedIntegration as any).provider || ''}
              </div>
              {(selectedIntegration as any).version && (
                <div className="text-xs text-datumbim-textSecondary">
                  Version: {(selectedIntegration as any).version}
                </div>
              )}
              {(selectedIntegration as any).error && (
                <div className="text-xs text-red-400">
                  Error: {(selectedIntegration as any).error}
                </div>
              )}
              {(selectedIntegration as any).capabilities && (selectedIntegration as any).capabilities.length > 0 && (
                <div className="space-y-1">
                  <div className="text-[10px] font-semibold text-datumbim-textSecondary uppercase">Capabilities</div>
                  {(selectedIntegration as any).capabilities.map((cap: any) => (
                    <div key={cap.capability_id} className="text-[10px] p-1 rounded border border-datumbim-border flex items-center justify-between">
                      <span className="text-datumbim-text">{cap.name}</span>
                      <span className={`text-[10px] ${cap.available ? 'text-green-400' : 'text-red-400'}`}>
                        {cap.available ? 'ON' : 'OFF'}
                      </span>
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
          {selectedIntegration && activeTab === 'integrations' ? (
            <div className="space-y-2">
              <button
                onClick={() => handleConnect((selectedIntegration as any).integration_id)}
                className="w-full text-xs px-2 py-1 bg-datumbim-accent text-white rounded hover:bg-datumbim-accent/80"
              >
                Connect
              </button>
              <button
                onClick={() => handleDisconnect((selectedIntegration as any).integration_id)}
                className="w-full text-xs px-2 py-1 bg-datumbim-border text-datumbim-text rounded hover:bg-datumbim-border/80"
              >
                Disconnect
              </button>
            </div>
          ) : (
            <div className="text-xs text-datumbim-textSecondary text-center py-4">
              {activeTab === 'integrations' ? 'Select an integration to manage' : 'No actions available'}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
