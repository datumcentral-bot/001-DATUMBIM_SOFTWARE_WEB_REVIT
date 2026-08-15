'use client'

import React, { useState, useCallback, useEffect } from 'react'
import { useShellStore } from '@/store/shellStore'
import { projectApi } from '@/lib/api/projects'
import { levelApi } from '@/lib/api/levels'
import { documentApi } from '@/lib/api/documents'
import type { ProjectResponse, LevelResponse, DocumentResponse } from '@/types/api'

interface ProjectNode {
  id: string
  label: string
  type: 'project' | 'folder' | 'model' | 'view' | 'sheet' | 'level' | 'category' | 'document'
  children?: ProjectNode[]
  expanded?: boolean
}

export default function ProjectBrowser() {
  const [tree, setTree] = useState<ProjectNode[]>([])
  const [loading, setLoading] = useState(false)
  const { addNotification, setActiveViewTab, pushNavigation, project } = useShellStore()

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
        const [levelRes, docRes] = await Promise.all([
          levelApi.list(project.id),
          documentApi.list(project.id),
        ])

        const levels: ProjectNode[] = (levelRes.data as LevelResponse[] | undefined)?.map((level) => ({
          id: level.id,
          label: level.name,
          type: 'level' as const,
        })) || []

        const docs: ProjectNode[] = (docRes.data as DocumentResponse[] | undefined)?.map((doc) => ({
          id: doc.id,
          label: doc.name,
          type: 'document' as const,
        })) || []

        return {
          id: project.id,
          label: project.name,
          type: 'project',
          expanded: true,
          children: [
            {
              id: `${project.id}-views`,
              label: 'Views',
              type: 'folder',
              expanded: true,
              children: [
                { id: `${project.id}-3d`, label: '{3D}', type: 'view' },
                { id: `${project.id}-floor`, label: 'Floor Plans', type: 'folder', expanded: false, children: levels.map(l => ({ id: l.id, label: l.label, type: 'view' as const })) },
                { id: `${project.id}-elev`, label: 'Elevations', type: 'folder', expanded: false, children: [
                  { id: `${project.id}-elev-north`, label: 'North', type: 'view' },
                  { id: `${project.id}-elev-south`, label: 'South', type: 'view' },
                  { id: `${project.id}-elev-east`, label: 'East', type: 'view' },
                  { id: `${project.id}-elev-west`, label: 'West', type: 'view' },
                ]},
                { id: `${project.id}-sect`, label: 'Sections', type: 'folder', expanded: false, children: [
                  { id: `${project.id}-sect-1`, label: 'Section 1', type: 'view' },
                ]},
              ],
            },
            {
              id: `${project.id}-sheets`,
              label: 'Sheets',
              type: 'folder',
              expanded: false,
              children: [],
            },
            {
              id: `${project.id}-levels`,
              label: 'Levels',
              type: 'folder',
              expanded: false,
              children: levels,
            },
            {
              id: `${project.id}-families`,
              label: 'Families',
              type: 'folder',
              expanded: false,
              children: [
                { id: `${project.id}-fam-walls`, label: 'Walls', type: 'category' },
                { id: `${project.id}-fam-doors`, label: 'Doors', type: 'category' },
                { id: `${project.id}-fam-windows`, label: 'Windows', type: 'category' },
                { id: `${project.id}-fam-floors`, label: 'Floors', type: 'category' },
                { id: `${project.id}-fam-roofs`, label: 'Roofs', type: 'category' },
                { id: `${project.id}-fam-cols`, label: 'Columns', type: 'category' },
                { id: `${project.id}-fam-beams`, label: 'Beams', type: 'category' },
                { id: `${project.id}-fam-ducts`, label: 'Ducts', type: 'category' },
                { id: `${project.id}-fam-pipes`, label: 'Pipes', type: 'category' },
              ],
            },
            {
              id: `${project.id}-categories`,
              label: 'Categories',
              type: 'folder',
              expanded: false,
              children: [
                { id: `${project.id}-cat-walls`, label: 'Walls', type: 'category' },
                { id: `${project.id}-cat-doors`, label: 'Doors', type: 'category' },
                { id: `${project.id}-cat-windows`, label: 'Windows', type: 'category' },
                { id: `${project.id}-cat-floors`, label: 'Floors', type: 'category' },
                { id: `${project.id}-cat-roofs`, label: 'Roofs', type: 'category' },
                { id: `${project.id}-cat-cols`, label: 'Structural Columns', type: 'category' },
                { id: `${project.id}-cat-beams`, label: 'Structural Framing', type: 'category' },
                { id: `${project.id}-cat-ducts`, label: 'Ducts', type: 'category' },
                { id: `${project.id}-cat-pipes`, label: 'Pipes', type: 'category' },
                { id: `${project.id}-cat-cable`, label: 'Cable Trays', type: 'category' },
                { id: `${project.id}-cat-conduits`, label: 'Conduits', type: 'category' },
              ],
            },
            {
              id: `${project.id}-docs`,
              label: 'Documents',
              type: 'folder',
              expanded: false,
              children: docs,
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
    if (node.type === 'view') {
      setActiveViewTab(node.id)
      pushNavigation(node.id)
      addNotification({ type: 'info', message: `Navigated to: ${node.label}` })
    } else if (node.type === 'level') {
      setActiveViewTab(node.id)
      pushNavigation(node.id)
      addNotification({ type: 'info', message: `Navigated to level: ${node.label}` })
    } else if (node.type === 'project') {
      addNotification({ type: 'info', message: `Selected project: ${node.label}` })
    } else if (node.type === 'category') {
      addNotification({ type: 'info', message: `Filter by category: ${node.label}` })
    } else if (node.type === 'document') {
      addNotification({ type: 'info', message: `Document: ${node.label}` })
    } else {
      addNotification({ type: 'info', message: `Selected: ${node.label}` })
    }
  }, [addNotification, setActiveViewTab, pushNavigation])

  const renderNode = (node: ProjectNode, depth = 0) => {
    const isProject = node.type === 'project'
    const isFolder = node.type === 'folder'
    const isView = node.type === 'view'
    const isLevel = node.type === 'level'
    const isCategory = node.type === 'category'

    let icon = '📁'
    if (isProject) icon = '📂'
    else if (isView) icon = '👁'
    else if (isLevel) icon = '📏'
    else if (isCategory) icon = '📊'
    else if (node.type === 'document') icon = '📄'

    return (
      <div key={node.id}>
        <button
          onClick={() => {
            if (node.children) toggleNode(node.id)
            else selectNode(node)
          }}
          onDoubleClick={() => {
            if (isView || isLevel) selectNode(node)
          }}
          className={`w-full flex items-center gap-1 px-2 py-1 text-xs hover:bg-datumbim-border/40 text-left ${
            isProject ? 'font-semibold text-datumbim-text' :
            isView || isLevel ? 'text-datumbim-text' :
            'text-datumbim-textSecondary'
          }`}
          style={{ paddingLeft: `${depth * 14 + 8}px` }}
        >
          {node.children && (
            <span className="w-4 text-[10px] text-datumbim-textSecondary flex-shrink-0">
              {node.expanded ? '▼' : '▶'}
            </span>
          )}
          {!node.children && <span className="w-4 text-[10px] flex-shrink-0">{icon}</span>}
          <span className="truncate">{node.label}</span>
        </button>
        {node.expanded && node.children && (
          <div>{node.children.map((child) => renderNode(child, depth + 1))}</div>
        )}
      </div>
    )
  }

  return (
    <div className="w-64 bg-datumbim-surface border-r border-datumbim-border flex flex-col h-full">
      <div className="h-8 border-b border-datumbim-border flex items-center justify-between px-3">
        <span className="text-[11px] font-semibold text-datumbim-textSecondary uppercase tracking-wider">
          Project Browser
        </span>
        <div className="flex items-center gap-1">
          <button
            onClick={loadProjects}
            className="text-[10px] text-datumbim-textSecondary hover:text-datumbim-text w-4 h-4 flex items-center justify-center rounded hover:bg-datumbim-border/50"
            disabled={loading}
            title="Refresh"
          >
            {loading ? '...' : '↻'}
          </button>
          <button
            onClick={() => addNotification({ type: 'info', message: 'Search not yet implemented' })}
            className="text-[10px] text-datumbim-textSecondary hover:text-datumbim-text w-4 h-4 flex items-center justify-center rounded hover:bg-datumbim-border/50"
            title="Search"
          >
            🔍
          </button>
        </div>
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
