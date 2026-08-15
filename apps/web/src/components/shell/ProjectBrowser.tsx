'use client'

import React, { useState, useCallback } from 'react'
import { useShellStore } from '@/store/shellStore'

interface ProjectNode {
  id: string
  label: string
  type: 'project' | 'folder' | 'model' | 'view' | 'sheet'
  children?: ProjectNode[]
  expanded?: boolean
}

const DEMO_TREE: ProjectNode[] = [
  {
    id: 'p1',
    label: 'Sample Project',
    type: 'project',
    expanded: true,
    children: [
      {
        id: 'p1-views',
        label: 'Views',
        type: 'folder',
        expanded: true,
        children: [
          { id: 'v1', label: '{3D}', type: 'view' },
          { id: 'v2', label: 'Floor Plan - Level 1', type: 'view' },
          { id: 'v3', label: 'Floor Plan - Level 2', type: 'view' },
          { id: 'v4', label: 'Elevation - North', type: 'view' },
          { id: 'v5', label: 'Section - A-A', type: 'view' },
        ],
      },
      {
        id: 'p1-sheets',
        label: 'Sheets',
        type: 'folder',
        expanded: false,
        children: [
          { id: 's1', label: 'A101 - Floor Plan', type: 'sheet' },
          { id: 's2', label: 'A201 - Elevations', type: 'sheet' },
        ],
      },
      {
        id: 'p1-models',
        label: 'Models',
        type: 'folder',
        expanded: false,
        children: [
          { id: 'm1', label: 'Architecture.rvt', type: 'model' },
          { id: 'm2', label: 'Structure.rvt', type: 'model' },
        ],
      },
    ],
  },
]

export default function ProjectBrowser() {
  const [tree, setTree] = useState<ProjectNode[]>(DEMO_TREE)
  const { addNotification, setActiveViewTab, pushNavigation } = useShellStore()

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
    } else if (node.type === 'sheet') {
      addNotification({ type: 'info', message: `Opened sheet: ${node.label}` })
    } else if (node.type === 'model') {
      addNotification({ type: 'info', message: `Opened model: ${node.label}` })
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
      <div className="h-8 border-b border-datumbim-border flex items-center px-3">
        <span className="text-[11px] font-semibold text-datumbim-textSecondary uppercase tracking-wider">
          Project Browser
        </span>
      </div>
      <div className="flex-1 overflow-auto py-1">
        {tree.map((node) => renderNode(node))}
      </div>
    </div>
  )
}
