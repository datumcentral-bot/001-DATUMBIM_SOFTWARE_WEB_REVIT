'use client'

import React, { useState, useEffect } from 'react'
import { useShellStore } from '@/store/shellStore'
import type { ApplicationStatus, ApplicationCapability } from '@/lib/connectors/types/ConnectorTypes'
import { LocalApplicationDiscovery } from '@/lib/connectors/LocalApplicationDiscovery'

interface ApplicationCard {
  id: string
  name: string
  description: string
  status: ApplicationStatus
  version?: string
  capabilities: ApplicationCapability[]
}

const STATUS_COLORS: Record<ApplicationStatus, string> = {
  unknown: 'text-gray-400',
  discovered: 'text-yellow-400',
  configured: 'text-blue-400',
  connected: 'text-green-400',
  authenticated: 'text-green-400',
  available: 'text-green-400',
  executable: 'text-green-400',
  verified: 'text-green-400',
  error: 'text-red-400',
}

export default function ApplicationsScreen() {
  const { addNotification } = useShellStore()
  const [applications, setApplications] = useState<ApplicationCard[]>([])
  const [localApps, setLocalApps] = useState<ReturnType<LocalApplicationDiscovery['discover']>>([])
  const discovery = new LocalApplicationDiscovery()

  useEffect(() => {
    const discovered = discovery.discover()
    setLocalApps(discovered)
    const cards: ApplicationCard[] = discovered.map((app) => ({
      id: app.id,
      name: app.displayName,
      description: `Local application: ${app.executable}`,
      status: app.running ? 'connected' : 'discovered',
      version: app.version,
      capabilities: app.capabilities.map((cap) => ({
        id: `${app.id}-${cap}`,
        name: cap,
        description: `${app.displayName} ${cap} capability`,
        channel: 'api',
        riskLevel: 'medium',
        available: app.running,
      })),
    }))
    setApplications(cards)
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  const handleConnect = async (appId: string) => {
    addNotification({ type: 'info', message: `Connecting to ${appId}...` })
    setTimeout(() => {
      setApplications((prev) =>
        prev.map((app) =>
          app.id === appId ? { ...app, status: 'connected' as ApplicationStatus } : app
        )
      )
      addNotification({ type: 'success', message: `Connected to ${appId}` })
    }, 1000)
  }

  const handleDisconnect = async (appId: string) => {
    addNotification({ type: 'info', message: `Disconnecting from ${appId}...` })
    setTimeout(() => {
      setApplications((prev) =>
        prev.map((app) =>
          app.id === appId ? { ...app, status: 'discovered' as ApplicationStatus } : app
        )
      )
      addNotification({ type: 'success', message: `Disconnected from ${appId}` })
    }, 500)
  }

  return (
    <div className="h-full flex flex-col">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h2 className="text-sm font-semibold text-datumbim-text">Applications</h2>
          <p className="text-xs text-datumbim-textSecondary">Connected and available applications</p>
        </div>
      </div>
      <div className="flex-1 overflow-auto">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
          {applications.map((app) => (
            <div key={app.id} className="bg-datumbim-surface border border-datumbim-border rounded p-3">
              <div className="flex items-center justify-between mb-2">
                <div>
                  <div className="text-sm font-medium text-datumbim-text">{app.name}</div>
                  <div className="text-[10px] text-datumbim-textSecondary">{app.id}</div>
                </div>
                <span className={`text-[10px] font-medium ${STATUS_COLORS[app.status]}`}>
                  {app.status.toUpperCase()}
                </span>
              </div>
              <div className="text-[10px] text-datumbim-textSecondary mb-2">
                {app.description || 'No description'}
              </div>
              <div className="flex flex-wrap gap-1 mb-2">
                {app.capabilities.map((cap) => (
                  <span
                    key={cap.id}
                    className={`text-[10px] px-1.5 py-0.5 rounded border ${
                      cap.available
                        ? 'border-green-500/30 text-green-400 bg-green-500/10'
                        : 'border-gray-500/30 text-gray-400 bg-gray-500/10'
                    }`}
                  >
                    {cap.name}
                  </span>
                ))}
              </div>
              <div className="flex gap-2">
                {app.status === 'discovered' || app.status === 'configured' ? (
                  <button
                    onClick={() => handleConnect(app.id)}
                    className="text-[10px] px-2 py-1 bg-datumbim-accent text-white rounded hover:bg-datumbim-accent/80"
                  >
                    Connect
                  </button>
                ) : (
                  <button
                    onClick={() => handleDisconnect(app.id)}
                    className="text-[10px] px-2 py-1 bg-datumbim-border text-datumbim-text rounded hover:bg-datumbim-border/80"
                  >
                    Disconnect
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
