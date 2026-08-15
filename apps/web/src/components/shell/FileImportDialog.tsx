'use client'

import React, { useCallback, useEffect, useRef, useState } from 'react'
import { useShellStore } from '@/store/shellStore'
import { formatApi } from '@/lib/api/formats'
import type { FormatInfo, FormatUploadResponse, FormatDetectionResponse } from '@/types/formats'

export default function FileImportDialog() {
  const { dialogs, closeDialog } = useShellStore()
  const [formats, setFormats] = useState<FormatInfo[]>([])
  const [dragOver, setDragOver] = useState(false)
  const [uploading, setUploading] = useState(false)
  const [detection, setDetection] = useState<FormatDetectionResponse | null>(null)
  const [uploadResult, setUploadResult] = useState<FormatUploadResponse | null>(null)
  const [error, setError] = useState<string | null>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const dialog = dialogs.find((d) => d.id === 'file-import')

  useEffect(() => {
    if (dialog?.open) {
      formatApi.list().then((res) => {
        if (!res.error && res.data) {
          setFormats(res.data.formats as FormatInfo[])
        }
      })
    }
  }, [dialog?.open])

  const handleFile = useCallback(async (file: File) => {
    setUploading(true)
    setError(null)
    setDetection(null)
    setUploadResult(null)

    try {
      const detectRes = await formatApi.detect(file.name, file.type)
      if (!detectRes.error && detectRes.data) {
        setDetection(detectRes.data)
      }

      const uploadRes = await formatApi.upload(file)
      if (!uploadRes.error && uploadRes.data) {
        setUploadResult(uploadRes.data)
      } else {
        setError(uploadRes.error || 'Upload failed')
      }
    } catch (exc) {
      setError(exc instanceof Error ? exc.message : 'Unknown error')
    } finally {
      setUploading(false)
    }
  }, [])

  const onDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setDragOver(false)
    const file = e.dataTransfer.files[0]
    if (file) handleFile(file)
  }, [handleFile])

  const onFileChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) handleFile(file)
  }, [handleFile])

  if (!dialog?.open) return null

  return (
    <div className="fixed inset-0 z-50 bg-black/50" onClick={() => closeDialog('file-import')}>
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4 pointer-events-none">
        <div className="bg-datumbim-surface border border-datumbim-border rounded-lg shadow-2xl w-full max-w-2xl pointer-events-auto">
          <div className="flex items-center justify-between px-4 h-12 border-b border-datumbim-border">
            <h2 className="text-sm font-semibold text-datumbim-text">Import File</h2>
            <button
              onClick={() => closeDialog('file-import')}
              className="text-datumbim-textSecondary hover:text-datumbim-text text-sm"
            >
              ×
            </button>
          </div>
          <div className="p-4">
            <div
              onDrop={onDrop}
              onDragOver={(e) => { e.preventDefault(); setDragOver(true) }}
              onDragLeave={() => setDragOver(false)}
              onClick={() => fileInputRef.current?.click()}
              className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${
                dragOver ? 'border-datumbim-accent bg-datumbim-accent/10' : 'border-datumbim-border hover:border-datumbim-textSecondary'
              }`}
            >
              <input ref={fileInputRef} type="file" className="hidden" onChange={onFileChange} />
              <div className="text-2xl mb-2">📄</div>
              <div className="text-sm text-datumbim-textSecondary">
                Drop a file here or click to browse
              </div>
              <div className="text-[11px] text-datumbim-textSecondary mt-1">
                Supported: IFC, RVT, DWG, DXF, NWD, NWC, PDF, CSV, XLSX, JSON, XML, GLTF, GLB, OBJ, FBX
              </div>
            </div>

            {error && (
              <div className="mt-4 p-3 bg-red-900/20 border border-red-700 rounded text-xs text-red-300">
                {error}
              </div>
            )}

            {detection && (
              <div className="mt-4 p-3 bg-datumbim-bg border border-datumbim-border rounded">
                <div className="text-xs font-semibold text-datumbim-text mb-1">Detected Format</div>
                <div className="text-xs text-datumbim-textSecondary">
                  Format: <span className="text-datumbim-text">{detection.format}</span> | Category: <span className="text-datumbim-text">{detection.category}</span> | Confidence: <span className="text-datumbim-text">{Math.round(detection.confidence * 100)}%</span>
                </div>
              </div>
            )}

            {uploadResult && (
              <div className="mt-4 p-3 bg-datumbim-bg border border-datumbim-border rounded">
                <div className="text-xs font-semibold text-datumbim-text mb-1">Upload Result</div>
                <div className="text-xs text-datumbim-textSecondary">
                  File: <span className="text-datumbim-text">{uploadResult.filename}</span> | Size: <span className="text-datumbim-text">{uploadResult.size} bytes</span>
                </div>
                {uploadResult.preview && (
                  <div className="mt-2 text-[11px] text-datumbim-textSecondary bg-datumbim-surface p-2 rounded border border-datumbim-border font-mono">
                    {uploadResult.preview}
                  </div>
                )}
              </div>
            )}

            {formats.length > 0 && (
              <div className="mt-4">
                <div className="text-xs font-semibold text-datumbim-textSecondary mb-2">Supported Formats</div>
                <div className="flex flex-wrap gap-1">
                  {formats.map((f) => (
                    <span key={f.format} className="px-2 py-0.5 text-[10px] bg-datumbim-border rounded text-datumbim-textSecondary">
                      {f.format.toUpperCase()}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
          <div className="flex justify-end gap-2 px-4 py-3 border-t border-datumbim-border">
            <button
              onClick={() => closeDialog('file-import')}
              className="px-3 py-1.5 text-xs bg-datumbim-border text-datumbim-text rounded hover:bg-datumbim-border/80"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
