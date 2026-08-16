'use client'

import React, { useState, useEffect, useCallback } from 'react'
import { useShellStore } from '@/store/shellStore'
import type { ApplicationSession, ApplicationStatus } from '@/lib/connectors/types/ConnectorTypes'
import { connectorsApi } from '@/lib/api/connectors'

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
  const [loading, setLoading] = useState(false)

  const loadSessions = useCallback(async () => {
    setLoading(true)
    try {
      const data = await connectorsApi.listSessions()
      setSessions(data)
    } catch (e) {
      addNotification({ type: 'error', message: 'Failed to load sessions' })
    } finally {
      setLoading(false)
    }
  }, [addNotification])

  useEffect(() => {
    loadSessions()
  }, [loadSessions])

  const handleStart = async (applicationId: string) => {
    addNotification({ type: 'info', message: `Starting session for ${applicationId}...` })
    try {
      const response = await fetch(`/api/sessions/${encodeURIComponent(applicationId)}/start`, {
        method: 'POST',
      })
      if (!response.ok) throw new Error('Failed to start session')
      const data = await response.json()
      setSessions((prev) => [...prev, data.session])
      addNotification({ type: 'success', message: `Session started for ${applicationId}` })
    } catch (e) {
      addNotification({ type: 'error', message: `Failed to start session for ${applicationId}` })
    }
  }

  const handleAttach = async (applicationId: string) => {
    addNotification({ type: 'info', message: `Attaching to ${applicationId}...` })
    try {
      const response = await fetch(`/api/sessions/${encodeURIComponent(applicationId)}/attach`, {
        method: 'POST',
      })
      if (!response.ok) throw new Error('Failed to attach session')
      const data = await response.json()
      setSessions((prev) => [...prev, data.session])
      addNotification({ type: 'success', message: `Attached to ${applicationId}` })
    } catch (e) {
      addNotification({ type: 'error', message: `Failed to attach to ${applicationId}` })
    }
  }

  const handleDetach = async (sessionId: string) => {
    addNotification({ type: 'info', message: `Detaching session ${sessionId}...` })
    try {
      const response = await fetch(`/api/sessions/${encodeURIComponent(sessionId)}/detach`, {
        method: 'POST',
      })
      if (!response.ok) throw new Error('Failed to detach session')
      const data = await response.json()
      setSessions((prev) => prev.map((s) => (s.id === sessionId ? data.session : s)))
      addNotification({ type: 'success', message: 'Session detached' })
    } catch (e) {
      addNotification({ type: 'error', message: 'Failed to detach session' })
    }
  }

  const handleRestart = async (sessionId: string) => {
    addNotification({ type: 'info', message: `Restarting session ${sessionId}...` })
    try {
      const response = await fetch(`/api/sessions/${encodeURIComponent(sessionId)}/restart`, {
        method: 'POST',
      })
      if (!response.ok) throw new Error('Failed to restart session')
      const data = await response.json()
      setSessions((prev) => prev.map((s) => (s.id === sessionId ? data.session : s)))
      addNotification({ type: 'success', message: 'Session restarted' })
    } catch (e) {
      addNotification({ type: 'error', message: 'Failed to restart session' })
    }
  }

  const handleClose = async (sessionId: string) => {
    addNotification({ type: 'info', message: `Closing session ${sessionId}...` })
    try {
      const response = await fetch(`/api/sessions/${encodeURIComponent(sessionId)}`, {
        method: 'DELETE',
      })
      if (!response.ok) throw new Error('Failed to close session')
      setSessions((prev) => prev.filter((s) => s.id !== sessionId))
      if (selectedSession?.id === sessionId) {
        setSelectedSession(null)
      }
      addNotification({ type: 'success', message: 'Session closed' })
    } catch (e) {
      addNotification({ type: 'error', message: 'Failed to close session' })
    }
  }

  return (
    <div className="h-full flex flex-col">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h2 className="text-sm font-semibold text-datumbim-text">Live Sessions</h2>
          <p className="text-xs text-datumbim-textSecondary">Active application sessions</p>
        </div>
        <button
          onClick={loadSessions}
          disabled={loading}
          className="text-[10px] px-2 py-1 bg-datumbim-border text-datumbim-text rounded hover:bg-datumbim-border/80 disabled:opacity-50"
        >
          {loading ? 'Refreshing...' : 'Refresh'}
        </button>
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
              <div className="flex flex-wrap gap-2">
                <button
                  onClick={() => handleStart(selectedSession.applicationId)}
                  className="text-[10px] px-2 py-1 bg-green-600 text-white rounded hover:bg-green-500"
                >
                  Start
                </button>
                <button
                  onClick={() => handleAttach(selectedSession.applicationId)}
                  className="text-[10px] px-2 py-1 bg-blue-600 text-white rounded hover:bg-blue-500"
                >
                  Attach
                </button>
                <button
                  onClick={() => handleDetach(selectedSession.id)}
                  className="text-[10px] px-2 py-1 bg-yellow-600 text-white rounded hover:bg-yellow-500"
                >
                  Detach
                </button>
                <button
                  onClick={() => handleRestart(selectedSession.id)}
                  className="text-[10px] px-2 py-1 bg-purple-600 text-white rounded hover:bg-purple-500"
                >
                  Restart
                </button>
                <button
                  onClick={() => handleClose(selectedSession.id)}
                  className="text-[10px] px-2 py-1 bg-red-600 text-white rounded hover:bg-red-500"
                >
                  Close
                </button>
              </div>
            </div>
          ) : (
            <div className="text-xs text-datumbim-textSecondary text-center py-8">Select a session to view details</div>
          )}
        </div>
      </div>
    </div>
  )
}
