'use client'

import React, { useState, useCallback, useEffect } from 'react'
import { useShellStore } from '@/store/shellStore'
import { projectApi } from '@/lib/api/projects'
import { levelApi } from '@/lib/api/levels'
import type { ProjectResponse, LevelResponse } from '@/types/api'

interface ProjectNode {
  id: string
  label: string
  type: 'project' | 'folder' | 'model' | 'view' | 'sheet' | 'level'
  children?: ProjectNode[]
  expanded?: boolean
}

export default function ProjectBrowser() {
  const [tree, setTree] = useState<ProjectNode[]>([])
  const [loading, setLoading] = useState(false)
  const { addNotification, setActiveViewTab, pushNavigation } = useShellStore()

  const loadProjects = useCallback(async () => {
    setLoading(true)
    const res = await projectApi.list()
    if (res.error || !res.data) {
      addNotification({ type: 'error', message: res.error || 'Failed to load projects' })
      setLoading(false)
      return
    }
    const projects: ProjectNode[] = await Promise.all(
      (res.data as ProjectResponse[]).map(async (project) => {
        const levelRes = await levelApi.list(project.id)
        const levels: ProjectNode[] = (levelRes.data as LevelResponse[] | undefined)?.map((level) => ({
          id: level.id,
          label: level.name,
          type: 'level' as const,
        })) || []

        return {
          id: project.id,
          label: project.name,
          type: 'project',
          expanded: true,
          children: [
            {
              id: `${project.id}-levels`,
              label: 'Levels',
              type: 'folder',
              expanded: true,
              children: levels,
            },
          ],
        }
      })
    )
    setTree(projects)
    setLoading(false)
  }, [addNotification])

  useEffect(() => {
    loadProjects()
  }, [loadProjects])

  const toggleNode = useCallback((id: string) => {
    const toggle = (nodes: ProjectNode[]): ProjectNode[] =>
      nodes.map((node) => {
        if (node.id === id && node.children) {
          return { ...node, expanded: !node.expanded }
        }
        if (node.children) {
          return { ...node, children: toggle(node.children) }
        }
        return node
      })
    setTree(toggle(tree))
  }, [tree])

  const selectNode = useCallback((node: ProjectNode) => {
    if (node.type === 'level') {
      setActiveViewTab(node.id)
      pushNavigation(node.id)
      addNotification({ type: 'info', message: `Navigated to level: ${node.label}` })
    } else if (node.type === 'project') {
      addNotification({ type: 'info', message: `Selected project: ${node.label}` })
    } else {
      addNotification({ type: 'info', message: `Selected: ${node.label}` })
    }
  }, [addNotification, setActiveViewTab, pushNavigation])

  const renderNode = (node: ProjectNode, depth = 0) => (
    <div key={node.id}>
      <button
        onClick={() => {
          if (node.children) toggleNode(node.id)
          else selectNode(node)
        }}
        className={`w-full flex items-center gap-1 px-2 py-1 text-xs hover:bg-datumbim-border/40 text-left ${
          node.type === 'project' ? 'font-semibold text-datumbim-text' : 'text-datumbim-textSecondary'
        }`}
        style={{ paddingLeft: `${depth * 12 + 8}px` }}
      >
        {node.children && (
          <span className="w-4 text-[10px] text-datumbim-textSecondary">
            {node.expanded ? '▼' : '▶'}
          </span>
        )}
        <span className="truncate">{node.label}</span>
      </button>
      {node.expanded && node.children && (
        <div>{node.children.map((child) => renderNode(child, depth + 1))}</div>
      )}
    </div>
  )

  return (
    <div className="w-64 bg-datumbim-surface border-r border-datumbim-border flex flex-col h-full">
      <div className="h-8 border-b border-datumbim-border flex items-center justify-between px-3">
        <span className="text-[11px] font-semibold text-datumbim-textSecondary uppercase tracking-wider">
          Project Browser
        </span>
        <button
          onClick={loadProjects}
          className="text-[10px] text-datumbim-textSecondary hover:text-datumbim-text"
          disabled={loading}
        >
          {loading ? '...' : '↻'}
        </button>
      </div>
      <div className="flex-1 overflow-auto py-1">
        {tree.length === 0 && !loading ? (
          <div className="p-3 text-xs text-datumbim-textSecondary">No projects found</div>
        ) : (
          tree.map((node) => renderNode(node))
        )}
      </div>
    </div>
  )
}
