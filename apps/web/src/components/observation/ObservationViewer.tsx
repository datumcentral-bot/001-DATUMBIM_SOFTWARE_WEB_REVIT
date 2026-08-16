'use client'

import React from 'react'

interface ObservationViewerProps {
  capture: {
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
  } | null
  loading?: boolean
}

export default function ObservationViewer({ capture, loading = false }: ObservationViewerProps) {
  if (loading) {
    return (
      <div className="h-full flex items-center justify-center text-xs text-datumbim-textSecondary">
        Loading observation...
      </div>
    )
  }

  if (!capture) {
    return (
      <div className="h-full flex items-center justify-center text-xs text-datumbim-textSecondary">
        Select a capture to view observation
      </div>
    )
  }

  if (capture.error) {
    return (
      <div className="h-full flex flex-col">
        <div className="text-xs text-red-400 mb-2">Capture failed</div>
        <div className="text-[10px] text-datumbim-textSecondary">{capture.error}</div>
      </div>
    )
  }

  return (
    <div className="h-full flex flex-col">
      <div className="flex items-center justify-between mb-2">
        <div className="text-[10px] font-semibold text-datumbim-textSecondary uppercase tracking-wider">Observation</div>
        <span className="text-[10px] px-1.5 py-0.5 rounded bg-green-500/10 text-green-400">
          {capture.status?.toUpperCase()}
        </span>
      </div>
      <div className="flex-1 border border-datumbim-border rounded bg-datumbim-bg flex items-center justify-center">
        {capture.image_reference ? (
          <img
            src={capture.image_reference}
            alt={`Observation ${capture.capture_id}`}
            className="max-w-full max-h-full object-contain"
          />
        ) : (
          <div className="text-xs text-datumbim-textSecondary">No image reference available</div>
        )}
      </div>
      <div className="mt-2 space-y-1">
        <div className="text-[10px] text-datumbim-textSecondary">
          Application: {capture.application_id}
        </div>
        <div className="text-[10px] text-datumbim-textSecondary">
          Target: {capture.target_type}{capture.target_id ? ` (${capture.target_id})` : ''}
        </div>
        <div className="text-[10px] text-datumbim-textSecondary">
          {new Date(capture.timestamp).toLocaleString()} • {capture.format} • {capture.width}x{capture.height}
        </div>
        {capture.provider && (
          <div className="text-[10px] text-datumbim-textSecondary">Provider: {capture.provider}</div>
        )}
      </div>
    </div>
  )
}
