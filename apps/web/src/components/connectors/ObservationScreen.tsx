'use client'

import React, { useState, useEffect, useCallback } from 'react'
import { useShellStore } from '@/store/shellStore'
import type { ApplicationSession } from '@/lib/connectors/types/ConnectorTypes'

interface Capture {
  capture_id: string
  session_id: string
  application_id: string
  timestamp: string
  width: number
  height: number
  format: string
  metadata: Record<string, string>
}

export default function ObservationScreen() {
  const { addNotification } = useShellStore()
  const [sessions, setSessions] = useState<ApplicationSession[]>([])
  const [selectedSessionId, setSelectedSessionId] = useState<string | null>(null)
  const [captures, setCaptures] = useState<Capture[]>([])
  const [loading, setLoading] = useState(false)
  const [capturing, setCapturing] = useState(false)

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

  useEffect(() => {
    if (!selectedSessionId) return
    let cancelled = false
    ;(async () => {
      try {
        const response = await fetch(`/api/observation/sessions/${encodeURIComponent(selectedSessionId)}/captures`)
        if (!response.ok) throw new Error('Failed to load captures')
        const data = await response.json()
        if (!cancelled) setCaptures(data.captures ?? [])
      } catch (e) {
        if (!cancelled) addNotification({ type: 'error', message: 'Failed to load captures' })
      }
    })()
    return () => {
      cancelled = true
    }
  }, [selectedSessionId, addNotification])

  const handleCapture = async () => {
    if (!selectedSessionId) return
    setCapturing(true)
    try {
      const response = await fetch(`/api/observation/sessions/${encodeURIComponent(selectedSessionId)}/capture`, {
        method: 'POST',
      })
      if (!response.ok) throw new Error('Capture failed')
      const data = await response.json()
      setCaptures((prev) => [...prev, data.capture])
      addNotification({ type: 'success', message: 'Screen captured' })
    } catch (e) {
      addNotification({ type: 'error', message: 'Screen capture failed' })
    } finally {
      setCapturing(false)
    }
  }

  return (
    <div className="h-full flex flex-col">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h2 className="text-sm font-semibold text-datumbim-text">Observation</h2>
          <p className="text-xs text-datumbim-textSecondary">Application screen observation and capture</p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={loadSessions}
            disabled={loading}
            className="text-[10px] px-2 py-1 bg-datumbim-border text-datumbim-text rounded hover:bg-datumbim-border/80 disabled:opacity-50"
          >
            Refresh Sessions
          </button>
          <button
            onClick={handleCapture}
            disabled={!selectedSessionId || capturing}
            className="text-[10px] px-2 py-1 bg-datumbim-accent text-white rounded hover:bg-datumbim-accent/80 disabled:opacity-50"
          >
            {capturing ? 'Capturing...' : 'Capture Screen'}
          </button>
        </div>
      </div>
      <div className="flex-1 grid grid-cols-1 md:grid-cols-2 gap-3">
        <div className="space-y-2">
          <div className="text-[10px] font-semibold text-datumbim-textSecondary uppercase tracking-wider">Sessions</div>
          {sessions.map((session) => (
            <div
              key={session.id}
              className={`bg-datumbim-surface border rounded p-2 cursor-pointer transition-colors ${
                selectedSessionId === session.id ? 'border-datumbim-accent' : 'border-datumbim-border hover:border-datumbim-accent/50'
              }`}
              onClick={() => setSelectedSessionId(session.id)}
            >
              <div className="text-xs font-medium text-datumbim-text">{session.applicationId}</div>
              <div className="text-[10px] text-datumbim-textSecondary">{session.id}</div>
            </div>
          ))}
          {sessions.length === 0 && (
            <div className="text-xs text-datumbim-textSecondary text-center py-4">No sessions available</div>
          )}
        </div>
        <div className="bg-datumbim-surface border border-datumbim-border rounded p-3">
          <div className="text-[10px] font-semibold text-datumbim-textSecondary uppercase tracking-wider mb-2">Captures</div>
          {selectedSessionId ? (
            <div className="space-y-2">
              {captures.map((capture) => (
                <div key={capture.capture_id} className="border border-datumbim-border rounded p-2">
                  <div className="text-xs text-datumbim-text">{capture.application_id}</div>
                  <div className="text-[10px] text-datumbim-textSecondary">
                    {new Date(capture.timestamp).toLocaleString()} • {capture.format} • {capture.width}x{capture.height}
                  </div>
                </div>
              ))}
              {captures.length === 0 && (
                <div className="text-xs text-datumbim-textSecondary text-center py-4">No captures yet</div>
              )}
            </div>
          ) : (
            <div className="text-xs text-datumbim-textSecondary text-center py-8">Select a session to view captures</div>
          )}
        </div>
      </div>
    </div>
  )
}
