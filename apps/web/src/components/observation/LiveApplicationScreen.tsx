'use client'

import React, { useState, useEffect, useCallback, useRef } from 'react'
import { useShellStore } from '@/store/shellStore'
import { apiClient } from '@/lib/apiClient'

interface LiveApplicationScreenProps {
  sessionId?: string | null
  applicationId?: string | null
}

interface UIElement {
  id: string
  type: string
  label?: string
  text?: string
  bounding_box?: { x: number; y: number; width: number; height: number }
  confidence?: number
  clickable: boolean
  enabled: boolean
  visible: boolean
}

interface VisionResult {
  request_id: string
  observation_id: string
  provider_id?: string
  model_id?: string
  status: string
  confidence?: number
  application?: string
  window?: string
  screen_description?: string
  elements: UIElement[]
  regions: any[]
  text_blocks: any[]
  action_hints: any[]
  warnings: string[]
  processing_time?: number
  error?: string
}

interface Capture {
  capture_id: string
  session_id: string
  application_id: string
  target_type: string
  target_id?: string
  timestamp: string
  width: number
  height: number
  format: string
  status: string
  provider?: string
  metadata?: Record<string, string>
  error?: string
  image_reference?: string
}

export default function LiveApplicationScreen({ sessionId, applicationId }: LiveApplicationScreenProps) {
  const { addNotification } = useShellStore()
  const [sessions, setSessions] = useState<any[]>([])
  const [selectedSessionId, setSelectedSessionId] = useState<string | null>(sessionId || null)
  const [selectedApplicationId, setSelectedApplicationId] = useState<string | null>(applicationId || null)
  const [captures, setCaptures] = useState<Capture[]>([])
  const [selectedCapture, setSelectedCapture] = useState<Capture | null>(null)
  const [loading, setLoading] = useState(false)
  const [capturing, setCapturing] = useState(false)
  const [analyzing, setAnalyzing] = useState(false)
  const [visionResult, setVisionResult] = useState<VisionResult | null>(null)
  const [uiElements, setUiElements] = useState<UIElement[]>([])
  const [actionType, setActionType] = useState('window')
  const [isObserving, setIsObserving] = useState(false)
  const observationInterval = useRef<number | null>(null)

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
        if (!cancelled) {
          setCaptures(data.captures ?? [])
          setSelectedCapture(null)
          setVisionResult(null)
          setUiElements([])
        }
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
      const appId = selectedApplicationId || sessions.find(s => s.id === selectedSessionId)?.applicationId || ''
      const response = await fetch('/api/observation/capture', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: selectedSessionId,
          application_id: appId,
          target_type: actionType,
          target_id: actionType === 'window' ? undefined : undefined,
        }),
      })
      if (!response.ok) throw new Error('Capture failed')
      const data = await response.json()
      setCaptures((prev) => [...prev, data.capture])
      setSelectedCapture(data.capture)
      addNotification({ type: 'success', message: 'Observation captured' })
    } catch (e) {
      addNotification({ type: 'error', message: 'Observation capture failed' })
    } finally {
      setCapturing(false)
    }
  }

  const handleAnalyze = async () => {
    if (!selectedCapture) return
    setAnalyzing(true)
    try {
      const res = await apiClient.post<{ vision: VisionResult }>('/ai/vision/analyze', {
        observation_id: selectedCapture.capture_id,
        provider_id: undefined,
        model_id: undefined,
        instructions: 'Describe this screen and identify interactive elements',
        detect_ui: true,
        detect_text: true,
        detect_regions: true,
        describe_application: true,
        generate_action_hints: true,
      })
      if (res.error || !res.data) throw new Error(res.error || 'Analysis failed')
      setVisionResult(res.data.vision)
      setUiElements(res.data.vision.elements)
      addNotification({ type: 'success', message: 'AI analysis completed' })
    } catch (e) {
      addNotification({ type: 'error', message: 'AI analysis failed' })
    } finally {
      setAnalyzing(false)
    }
  }

  const toggleObservation = () => {
    if (isObserving) {
      if (observationInterval.current) {
        clearInterval(observationInterval.current)
        observationInterval.current = null
      }
      setIsObserving(false)
      addNotification({ type: 'info', message: 'Observation paused' })
    } else {
      handleCapture()
      observationInterval.current = window.setInterval(() => {
        handleCapture()
      }, 2000)
      setIsObserving(true)
      addNotification({ type: 'info', message: 'Observation started' })
    }
  }

  useEffect(() => {
    return () => {
      if (observationInterval.current) {
        clearInterval(observationInterval.current)
      }
    }
  }, [])

  return (
    <div className="h-full flex flex-col">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h2 className="text-sm font-semibold text-datumbim-text">Live Application</h2>
          <p className="text-xs text-datumbim-textSecondary">Real application screen observation and control</p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={loadSessions}
            disabled={loading}
            className="text-[10px] px-2 py-1 bg-datumbim-border text-datumbim-text rounded hover:bg-datumbim-border/80 disabled:opacity-50"
          >
            Refresh
          </button>
          <button
            onClick={toggleObservation}
            disabled={!selectedSessionId}
            className={`text-[10px] px-2 py-1 rounded hover:opacity-80 disabled:opacity-50 ${
              isObserving ? 'bg-red-500 text-white' : 'bg-datumbim-accent text-white'
            }`}
          >
            {isObserving ? 'Stop' : 'Observe'}
          </button>
          <button
            onClick={handleCapture}
            disabled={!selectedSessionId || capturing}
            className="text-[10px] px-2 py-1 bg-datumbim-accent text-white rounded hover:bg-datumbim-accent/80 disabled:opacity-50"
          >
            {capturing ? 'Capturing...' : 'Capture'}
          </button>
        </div>
      </div>
      <div className="flex-1 grid grid-cols-1 md:grid-cols-3 gap-3">
        <div className="bg-datumbim-surface border border-datumbim-border rounded p-3 flex flex-col">
          <div className="text-[10px] font-semibold text-datumbim-textSecondary uppercase tracking-wider mb-2">Sessions</div>
          <div className="space-y-2 flex-1 overflow-auto">
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
        <div className="bg-datumbim-surface border border-datumbim-border rounded p-3 flex flex-col">
          <div className="text-[10px] font-semibold text-datumbim-textSecondary uppercase tracking-wider mb-2">Live View</div>
          <div className="flex-1 border border-datumbim-border rounded bg-datumbim-bg flex items-center justify-center overflow-hidden">
            {selectedCapture?.image_reference ? (
              <img
                src={selectedCapture.image_reference}
                alt={`Live view ${selectedCapture.capture_id}`}
                className="max-w-full max-h-full object-contain"
              />
            ) : (
              <div className="text-xs text-datumbim-textSecondary">No capture available</div>
            )}
          </div>
          <div className="mt-2 flex gap-2">
            <select
              value={actionType}
              onChange={(e) => setActionType(e.target.value)}
              className="text-[10px] p-1 rounded border border-datumbim-border bg-datumbim-bg text-datumbim-text"
            >
              <option value="window">Window</option>
              <option value="full_screen">Full Screen</option>
              <option value="region">Region</option>
              <option value="application">Application</option>
            </select>
            <button
              onClick={handleAnalyze}
              disabled={!selectedCapture || analyzing}
              className="text-[10px] px-2 py-1 bg-datumbim-accent text-white rounded hover:bg-datumbim-accent/80 disabled:opacity-50"
            >
              {analyzing ? 'Analyzing...' : 'Analyze'}
            </button>
          </div>
        </div>
        <div className="bg-datumbim-surface border border-datumbim-border rounded p-3 flex flex-col">
          <div className="text-[10px] font-semibold text-datumbim-textSecondary uppercase tracking-wider mb-2">AI Observation</div>
          <div className="flex-1 overflow-auto space-y-2">
            {visionResult ? (
              <>
                <div className={`text-[10px] px-1.5 py-0.5 rounded inline-block ${visionResult.status === 'completed' ? 'bg-green-500/10 text-green-400' : 'bg-red-500/10 text-red-400'}`}>
                  {visionResult.status.toUpperCase()}
                </div>
                {visionResult.screen_description && (
                  <div className="text-[10px] text-datumbim-textSecondary">{visionResult.screen_description}</div>
                )}
                <div className="text-[10px] text-datumbim-textSecondary">
                  Elements: {visionResult.elements.length} • Regions: {visionResult.regions.length} • Text blocks: {visionResult.text_blocks.length}
                </div>
                {visionResult.elements.length > 0 && (
                  <div className="space-y-1">
                    {visionResult.elements.map((element) => (
                      <div key={element.id} className="text-[10px] p-1 rounded border border-datumbim-border">
                        <div className="text-datumbim-text">{element.label || element.type}</div>
                        <div className="text-datumbim-textSecondary">
                          {element.type} • Clickable: {element.clickable ? 'Yes' : 'No'} • Confidence: {element.confidence?.toFixed(2)}
                        </div>
                      </div>
                    ))}
                  </div>
                )}
                {visionResult.action_hints.length > 0 && (
                  <div className="space-y-1">
                    {visionResult.action_hints.map((hint) => (
                      <div key={hint.element_id} className="text-[10px] p-1 rounded border border-yellow-500/30 bg-yellow-500/10 text-yellow-400">
                        {hint.action_type}: {hint.description}
                      </div>
                    ))}
                  </div>
                )}
              </>
            ) : (
              <div className="text-xs text-datumbim-textSecondary">Capture and analyze to see AI observation</div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
