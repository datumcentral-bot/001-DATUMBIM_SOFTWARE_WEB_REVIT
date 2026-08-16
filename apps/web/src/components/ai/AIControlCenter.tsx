'use client'

import React, { useState, useEffect, useCallback } from 'react'
import { useShellStore } from '@/store/shellStore'
import { apiClient } from '@/lib/apiClient'

interface AIProvider {
  provider_id: string
  display_name: string
  status: string
  supports_vision: boolean
  supports_tools: boolean
}

interface AIModel {
  provider_id: string
  model_id: string
  display_name: string
  capabilities: string[]
  vision_supported: boolean
  tool_calling_supported: boolean
  structured_output_supported: boolean
  local: boolean
  availability: string
}

interface VisionElement {
  id: string
  type: string
  label?: string
  text?: string
  bounding_box?: { x: number; y: number; width: number; height: number }
  confidence?: number
  clickable: boolean
  enabled: boolean
  visible: boolean
  role?: string
}

interface VisionResponse {
  request_id: string
  observation_id: string
  provider_id?: string
  model_id?: string
  status: string
  confidence?: number
  application?: string
  window?: string
  screen_description?: string
  elements: VisionElement[]
  regions: any[]
  text_blocks: any[]
  action_hints: any[]
  warnings: string[]
  processing_time?: number
  usage?: Record<string, any>
  raw_reference?: string
  error?: string
}

export default function AIControlCenter() {
  const { addNotification } = useShellStore()
  const [providers, setProviders] = useState<AIProvider[]>([])
  const [models, setModels] = useState<AIModel[]>([])
  const [health, setHealth] = useState<Record<string, any>>({})
  const [selectedProvider, setSelectedProvider] = useState<string | null>(null)
  const [selectedModel, setSelectedModel] = useState<string | null>(null)
  const [instructions, setInstructions] = useState('Describe this screen and identify interactive elements')
  const [visionResult, setVisionResult] = useState<VisionResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [analyzing, setAnalyzing] = useState(false)

  const loadProviders = useCallback(async () => {
    setLoading(true)
    try {
      const res = await apiClient.get<{ providers: AIProvider[] }>('/ai/providers')
      if (res.error) throw new Error(res.error)
      setProviders(res.data?.providers ?? [])
    } catch (e) {
      addNotification({ type: 'error', message: 'Failed to load AI providers' })
    } finally {
      setLoading(false)
    }
  }, [addNotification])

  const loadModels = useCallback(async () => {
    setLoading(true)
    try {
      const res = await apiClient.get<{ models: AIModel[] }>('/ai/models')
      if (res.error) throw new Error(res.error)
      setModels(res.data?.models ?? [])
    } catch (e) {
      addNotification({ type: 'error', message: 'Failed to load AI models' })
    } finally {
      setLoading(false)
    }
  }, [addNotification])

  const loadHealth = useCallback(async () => {
    setLoading(true)
    try {
      const res = await apiClient.get<{ providers: Record<string, any> }>('/ai/health')
      if (res.error) throw new Error(res.error)
      setHealth(res.data?.providers ?? {})
    } catch (e) {
      addNotification({ type: 'error', message: 'Failed to load AI health' })
    } finally {
      setLoading(false)
    }
  }, [addNotification])

  useEffect(() => {
    loadProviders()
    loadModels()
    loadHealth()
  }, [loadProviders, loadModels, loadHealth])

  const handleAnalyze = async () => {
    setAnalyzing(true)
    try {
      const res = await apiClient.post<{ vision: VisionResponse }>('/ai/vision/analyze', {
        observation_id: 'obs-1',
        provider_id: selectedProvider,
        model_id: selectedModel,
        instructions,
        detect_ui: true,
        detect_text: true,
        detect_regions: true,
        describe_application: true,
        generate_action_hints: true,
      })
      if (res.error || !res.data) throw new Error(res.error || 'Analysis failed')
      setVisionResult(res.data.vision)
      addNotification({ type: 'success', message: 'AI analysis completed' })
    } catch (e) {
      addNotification({ type: 'error', message: 'AI analysis failed' })
    } finally {
      setAnalyzing(false)
    }
  }

  const providerHealth = (providerId: string) => health[providerId]

  return (
    <div className="h-full flex flex-col">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h2 className="text-sm font-semibold text-datumbim-text">AI Control Center</h2>
          <p className="text-xs text-datumbim-textSecondary">Multi-model AI vision and understanding</p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={loadProviders}
            disabled={loading}
            className="text-[10px] px-2 py-1 bg-datumbim-border text-datumbim-text rounded hover:bg-datumbim-border/80 disabled:opacity-50"
          >
            Refresh Providers
          </button>
        </div>
      </div>
      <div className="flex-1 grid grid-cols-1 md:grid-cols-3 gap-3">
        <div className="bg-datumbim-surface border border-datumbim-border rounded p-3">
          <div className="text-[10px] font-semibold text-datumbim-textSecondary uppercase tracking-wider mb-2">Providers</div>
          <div className="space-y-2">
            {providers.map((provider) => {
              const healthInfo = providerHealth(provider.provider_id)
              const statusColor = provider.status === 'available' ? 'text-green-400' : provider.status === 'auth_required' ? 'text-yellow-400' : 'text-red-400'
              return (
                <div
                  key={provider.provider_id}
                  className={`text-xs p-2 rounded border cursor-pointer ${
                    selectedProvider === provider.provider_id ? 'border-datumbim-accent bg-datumbim-accent/10' : 'border-datumbim-border'
                  }`}
                  onClick={() => setSelectedProvider(provider.provider_id)}
                >
                  <div className="font-medium text-datumbim-text">{provider.display_name}</div>
                  <div className={`text-[10px] ${statusColor}`}>{provider.status.toUpperCase()}</div>
                  <div className="text-[10px] text-datumbim-textSecondary">
                    Vision: {provider.supports_vision ? 'Yes' : 'No'} • Tools: {provider.supports_tools ? 'Yes' : 'No'}
                  </div>
                </div>
              )
            })}
            {providers.length === 0 && (
              <div className="text-xs text-datumbim-textSecondary text-center py-4">No providers available</div>
            )}
          </div>
        </div>
        <div className="bg-datumbim-surface border border-datumbim-border rounded p-3">
          <div className="text-[10px] font-semibold text-datumbim-textSecondary uppercase tracking-wider mb-2">Models</div>
          <div className="space-y-2">
            {models.map((model) => (
              <div
                key={`${model.provider_id}-${model.model_id}`}
                className={`text-xs p-2 rounded border cursor-pointer ${
                  selectedModel === model.model_id ? 'border-datumbim-accent bg-datumbim-accent/10' : 'border-datumbim-border'
                }`}
                onClick={() => setSelectedModel(model.model_id)}
              >
                <div className="font-medium text-datumbim-text">{model.display_name}</div>
                <div className="text-[10px] text-datumbim-textSecondary">{model.provider_id}</div>
                <div className="text-[10px] text-datumbim-textSecondary">
                  {model.availability.toUpperCase()} • Vision: {model.vision_supported ? 'Yes' : 'No'}
                </div>
              </div>
            ))}
            {models.length === 0 && (
              <div className="text-xs text-datumbim-textSecondary text-center py-4">No models available</div>
            )}
          </div>
        </div>
        <div className="bg-datumbim-surface border border-datumbim-border rounded p-3">
          <div className="text-[10px] font-semibold text-datumbim-textSecondary uppercase tracking-wider mb-2">Vision Analysis</div>
          <div className="space-y-2">
            <div>
              <label className="text-[10px] text-datumbim-textSecondary">Instructions</label>
              <textarea
                value={instructions}
                onChange={(e) => setInstructions(e.target.value)}
                className="w-full mt-1 text-xs p-1 rounded border border-datumbim-border bg-datumbim-bg text-datumbim-text"
                rows={3}
              />
            </div>
            <button
              onClick={handleAnalyze}
              disabled={analyzing}
              className="w-full text-xs px-2 py-1 bg-datumbim-accent text-white rounded hover:bg-datumbim-accent/80 disabled:opacity-50"
            >
              {analyzing ? 'Analyzing...' : 'Analyze Observation'}
            </button>
            {visionResult && (
              <div className="mt-2 space-y-2">
                <div className="text-[10px] font-semibold text-datumbim-textSecondary uppercase tracking-wider">Result</div>
                <div className={`text-[10px] px-1.5 py-0.5 rounded ${visionResult.status === 'completed' ? 'bg-green-500/10 text-green-400' : 'bg-red-500/10 text-red-400'}`}>
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
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
