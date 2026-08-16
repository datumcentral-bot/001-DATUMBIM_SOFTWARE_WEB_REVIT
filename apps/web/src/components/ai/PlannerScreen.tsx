'use client'

import React, { useState } from 'react'
import { useShellStore } from '@/store/shellStore'
import { apiClient } from '@/lib/apiClient'

interface ActionStep {
  action_id: string
  sequence: number
  action_type: string
  description: string
  application_id?: string
  session_id?: string
  parameters: Record<string, any>
  preconditions: string[]
  expected_result?: string
  verification_strategy?: string
  risk_level: string
  approval_required: boolean
  reversible: boolean
  estimated_duration?: number
  dependencies: string[]
  confidence?: number
  source: string
  status: string
}

interface Plan {
  plan_id: string
  goal_id: string
  title: string
  objective: string
  summary: string
  application_id?: string
  session_id?: string
  actions: ActionStep[]
  dependencies: Record<string, string[]>
  risk_level: string
  approval_required: boolean
  estimated_duration?: number
  confidence?: number
  expected_observations: string[]
  success_criteria: string[]
  rollback_strategy?: string
  planner_provider?: string
  planner_model?: string
  created_at: string
  status: string
}

export default function PlannerScreen() {
  const { addNotification } = useShellStore()
  const [goal, setGoal] = useState('Open Revit and inspect Level 2')
  const [applicationId, setApplicationId] = useState('revit')
  const [sessionId, setSessionId] = useState('')
  const [plan, setPlan] = useState<Plan | null>(null)
  const [plans, setPlans] = useState<Plan[]>([])
  const [loading, setLoading] = useState(false)
  const [explanation, setExplanation] = useState('')

  const handlePlan = async () => {
    if (!goal.trim()) return
    setLoading(true)
    try {
      const res = await apiClient.post<{ plan: Plan }>('/planner/plan', {
        user_request: goal,
        application_id: applicationId || null,
        session_id: sessionId || null,
        dry_run: false,
      })
      if (res.error || !res.data) throw new Error(res.error || 'Planning failed')
      setPlan(res.data.plan)
      setPlans(prev => [res.data!.plan, ...prev])
      addNotification({ type: 'success', message: 'Plan generated' })
    } catch (e) {
      addNotification({ type: 'error', message: 'Planning failed' })
    } finally {
      setLoading(false)
    }
  }

  const handleExplain = async () => {
    if (!plan) return
    try {
      const res = await apiClient.post<{ explanation: string }>(`/planner/plans/${plan.plan_id}/explain`, {})
      if (res.error || !res.data) throw new Error(res.error || 'Explain failed')
      setExplanation(res.data.explanation)
    } catch (e) {
      addNotification({ type: 'error', message: 'Explain failed' })
    }
  }

  const handleValidate = async () => {
    if (!plan) return
    try {
      const res = await apiClient.post<{ validation: any }>(`/planner/plans/${plan.plan_id}/validate`, {})
      if (res.error || !res.data) throw new Error(res.error || 'Validate failed')
      addNotification({ type: 'success', message: res.data.validation.valid ? 'Plan is valid' : 'Plan has errors' })
    } catch (e) {
      addNotification({ type: 'error', message: 'Validation failed' })
    }
  }

  const loadPlans = async () => {
    setLoading(true)
    try {
      const res = await apiClient.get<{ plans: Plan[] }>('/planner/plans')
      if (res.error) throw new Error(res.error)
      setPlans(res.data?.plans ?? [])
    } catch (e) {
      addNotification({ type: 'error', message: 'Failed to load plans' })
    } finally {
      setLoading(false)
    }
  }

  const riskColor = (level: string) => {
    switch (level) {
      case 'low': return 'text-green-400'
      case 'medium': return 'text-yellow-400'
      case 'high': return 'text-orange-400'
      case 'critical': return 'text-red-400'
      default: return 'text-datumbim-textSecondary'
    }
  }

  return (
    <div className="h-full flex flex-col">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h2 className="text-sm font-semibold text-datumbim-text">AI Planner</h2>
          <p className="text-xs text-datumbim-textSecondary">Structured action proposals</p>
        </div>
        <div className="flex gap-2">
          <button onClick={loadPlans} disabled={loading} className="text-[10px] px-2 py-1 bg-datumbim-border text-datumbim-text rounded hover:bg-datumbim-border/80 disabled:opacity-50">
            Refresh Plans
          </button>
        </div>
      </div>
      <div className="flex-1 grid grid-cols-1 md:grid-cols-2 gap-3">
        <div className="bg-datumbim-surface border border-datumbim-border rounded p-3">
          <div className="text-[10px] font-semibold text-datumbim-textSecondary uppercase tracking-wider mb-2">Goal Input</div>
          <div className="space-y-2">
            <div>
              <label className="text-[10px] text-datumbim-textSecondary">User Request</label>
              <textarea value={goal} onChange={e => setGoal(e.target.value)} className="w-full mt-1 text-xs p-1 rounded border border-datumbim-border bg-datumbim-bg text-datumbim-text" rows={3} />
            </div>
            <div className="grid grid-cols-2 gap-2">
              <div>
                <label className="text-[10px] text-datumbim-textSecondary">Application</label>
                <input value={applicationId} onChange={e => setApplicationId(e.target.value)} className="w-full mt-1 text-xs p-1 rounded border border-datumbim-border bg-datumbim-bg text-datumbim-text" />
              </div>
              <div>
                <label className="text-[10px] text-datumbim-textSecondary">Session</label>
                <input value={sessionId} onChange={e => setSessionId(e.target.value)} className="w-full mt-1 text-xs p-1 rounded border border-datumbim-border bg-datumbim-bg text-datumbim-text" />
              </div>
            </div>
            <button onClick={handlePlan} disabled={loading} className="w-full text-xs px-2 py-1 bg-datumbim-accent text-white rounded hover:bg-datumbim-accent/80 disabled:opacity-50">
              {loading ? 'Planning...' : 'Generate Plan'}
            </button>
          </div>
        </div>
        <div className="bg-datumbim-surface border border-datumbim-border rounded p-3">
          <div className="text-[10px] font-semibold text-datumbim-textSecondary uppercase tracking-wider mb-2">Generated Plan</div>
          {plan ? (
            <div className="space-y-2">
              <div>
                <div className="text-xs font-medium text-datumbim-text">{plan.title}</div>
                <div className="text-[10px] text-datumbim-textSecondary">{plan.objective}</div>
              </div>
              <div className="flex gap-2">
                <span className={`text-[10px] px-1.5 py-0.5 rounded ${riskColor(plan.risk_level)} bg-datumbim-border`}>{plan.risk_level.toUpperCase()}</span>
                <span className="text-[10px] px-1.5 py-0.5 rounded bg-datumbim-border text-datumbim-textSecondary">{plan.status.toUpperCase()}</span>
              </div>
              <div className="space-y-1">
                {plan.actions.map(action => (
                  <div key={action.action_id} className="text-[10px] p-1.5 rounded border border-datumbim-border">
                    <div className="text-datumbim-text">{action.sequence}. {action.description}</div>
                    <div className="text-datumbim-textSecondary">
                      {action.action_type} • Risk: {action.risk_level} • Confidence: {action.confidence?.toFixed(2)}
                    </div>
                    <div className="text-datumbim-textSecondary">
                      Verification: {action.verification_strategy || 'none'} • Approval: {action.approval_required ? 'Yes' : 'No'}
                    </div>
                  </div>
                ))}
              </div>
              <div className="flex gap-2">
                <button onClick={handleValidate} className="text-[10px] px-2 py-1 bg-datumbim-border text-datumbim-text rounded hover:bg-datumbim-border/80">Validate</button>
                <button onClick={handleExplain} className="text-[10px] px-2 py-1 bg-datumbim-border text-datumbim-text rounded hover:bg-datumbim-border/80">Explain</button>
              </div>
              {explanation && (
                <pre className="text-[10px] p-1.5 rounded border border-datumbim-border bg-datumbim-bg text-datumbim-text whitespace-pre-wrap">{explanation}</pre>
              )}
            </div>
          ) : (
            <div className="text-xs text-datumbim-textSecondary text-center py-4">No plan generated yet</div>
          )}
        </div>
        <div className="bg-datumbim-surface border border-datumbim-border rounded p-3 md:col-span-2">
          <div className="text-[10px] font-semibold text-datumbim-textSecondary uppercase tracking-wider mb-2">Recent Plans</div>
          <div className="space-y-1">
            {plans.map(p => (
              <div key={p.plan_id} className="text-[10px] p-1.5 rounded border border-datumbim-border flex items-center justify-between">
                <div>
                  <span className="text-datumbim-text">{p.title}</span>
                  <span className="text-datumbim-textSecondary ml-2">{p.status}</span>
                </div>
                <span className={`text-[10px] ${riskColor(p.risk_level)}`}>{p.risk_level.toUpperCase()}</span>
              </div>
            ))}
            {plans.length === 0 && (
              <div className="text-xs text-datumbim-textSecondary text-center py-2">No plans yet</div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
