'use client'

import React, { useState, useEffect } from 'react'
import { useShellStore } from '@/store/shellStore'
import type { ApplicationSession, ApplicationStatus, ApplicationConnector } from '@/lib/connectors/types/ConnectorTypes'

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

export default function SessionsScreen() {
  const { addNotification } = useShellStore()
  const [sessions, setSessions] = useState<ApplicationSession[]>([])
  const [selectedSession, setSelectedSession] = useState<ApplicationSession | null>(null)

  useEffect(() => {
    const mockSessions: ApplicationSession[] = [
      {
        id: 'revit-session-1',
        applicationId: 'revit',
        status: 'connected',
        capabilities: [
          { id: 'revit-api', name: 'API', channel: 'api', riskLevel: 'medium', available: true },
          { id: 'revit-pyrevit', name: 'pyRevit', channel: 'plugin', riskLevel: 'medium', available: true },
          { id: 'revit-dynamo', name: 'Dynamo', channel: 'script', riskLevel: 'low', available: true },
        ],
      },
    ]
    setSessions(mockSessions)
  }, [])

  const handleDisconnect = async (sessionId: string) => {
    addNotification({ type: 'info', message: `Disconnecting session ${sessionId}...` })
    setTimeout(() => {
      setSessions((prev) => prev.filter((s) => s.id !== sessionId))
      if (selectedSession?.id === sessionId) {
        setSelectedSession(null)
      }
      addNotification({ type: 'success', message: 'Session disconnected' })
    }, 500)
  }

  return (
    <div className="h-full flex flex-col">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h2 className="text-sm font-semibold text-datumbim-text">Live Sessions</h2>
          <p className="text-xs text-datumbim-textSecondary">Active application sessions</p>
        </div>
      </div>
      <div className="flex-1 grid grid-cols-1 md:grid-cols-2 gap-3">
        <div className="space-y-2">
          {sessions.map((session) => (
            <div
              key={session.id}
              className={`bg-datumbim-surface border rounded p-3 cursor-pointer transition-colors ${
                selectedSession?.id === session.id
                  ? 'border-datumbim-accent'
                  : 'border-datumbim-border hover:border-datumbim-accent/50'
              }`}
              onClick={() => setSelectedSession(session)}
            >
              <div className="flex items-center justify-between mb-1">
                <div className="text-sm font-medium text-datumbim-text">{session.applicationId}</div>
                <span className={`text-[10px] font-medium ${STATUS_COLORS[session.status]}`}>
                  {session.status.toUpperCase()}
                </span>
              </div>
              <div className="text-[10px] text-datumbim-textSecondary">{session.id}</div>
            </div>
          ))}
          {sessions.length === 0 && (
            <div className="text-xs text-datumbim-textSecondary text-center py-4">No active sessions</div>
          )}
        </div>
        <div className="bg-datumbim-surface border border-datumbim-border rounded p-3">
          {selectedSession ? (
            <div>
              <div className="text-sm font-semibold text-datumbim-text mb-2">
                {selectedSession.applicationId} Session
              </div>
              <div className="text-[10px] text-datumbim-textSecondary mb-1">Session ID: {selectedSession.id}</div>
              <div className="text-[10px] text-datumbim-textSecondary mb-3">
                Status: {selectedSession.status.toUpperCase()}
              </div>
              <div className="mb-3">
                <div className="text-[10px] text-datumbim-textSecondary mb-1">Capabilities</div>
                <div className="flex flex-wrap gap-1">
                  {selectedSession.capabilities.map((cap) => (
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
              </div>
              <button
                onClick={() => handleDisconnect(selectedSession.id)}
                className="text-[10px] px-2 py-1 bg-datumbim-border text-datumbim-text rounded hover:bg-datumbim-border/80"
              >
                Disconnect
              </button>
            </div>
          ) : (
            <div className="text-xs text-datumbim-textSecondary text-center py-8">Select a session to view details</div>
          )}
        </div>
      </div>
    </div>
  )
}
