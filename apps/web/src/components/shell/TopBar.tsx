'use client'

import React, { useState, useRef, useEffect } from 'react'
import { useShellStore } from '@/store/shellStore'
import { projectApi } from '@/lib/api/projects'
import type { ProjectResponse } from '@/types/api'

export default function TopBar() {
  const { project, executeCommand, openDialog, addNotification } = useShellStore()
  const [menuOpen, setMenuOpen] = useState(false)
  const menuRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setMenuOpen(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  const handleNewProject = async () => {
    setMenuOpen(false)
    openDialog({ id: 'new-project', title: 'New Project', content: null })
  }

  const handleOpenProject = async () => {
    setMenuOpen(false)
    const res = await projectApi.list()
    if (res.error || !res.data) {
      addNotification({ type: 'error', message: res.error || 'Failed to load projects' })
      return
    }
    openDialog({ id: 'open-project', title: 'Open Project', content: null })
  }

  const handleSave = async () => {
    setMenuOpen(false)
    if (!project.id) {
      addNotification({ type: 'warning', message: 'No project open' })
      return
    }
    executeCommand('project.save')
  }

  return (
    <div className="h-9 bg-datumbim-ribbon border-b border-datumbim-border flex items-center px-2 select-none">
      <div className="flex items-center gap-2">
        <button
          onClick={handleNewProject}
          className="text-xs font-bold text-datumbim-text tracking-wide hover:bg-datumbim-border/50 px-2 py-1 rounded"
        >
          DATUMBIM
        </button>
        <span className="text-[10px] text-datumbim-textSecondary bg-datumbim-surface px-1.5 py-0.5 rounded border border-datumbim-border">
          WEB REVIT
        </span>
      </div>

      <div className="ml-4 flex items-center gap-1 border-l border-datumbim-border pl-3">
        <div className="relative" ref={menuRef}>
          <button
            onClick={() => setMenuOpen(!menuOpen)}
            className="text-xs text-datumbim-textSecondary hover:text-datumbim-text px-2 py-1 rounded hover:bg-datumbim-border/50"
          >
            File
          </button>
          {menuOpen && (
            <div className="absolute top-full left-0 mt-1 w-48 bg-datumbim-surface border border-datumbim-border rounded-md shadow-xl z-50 py-1">
              <button onClick={handleNewProject} className="w-full text-left px-3 py-1.5 text-xs text-datumbim-text hover:bg-datumbim-border/50">
                New Project
              </button>
              <button onClick={handleOpenProject} className="w-full text-left px-3 py-1.5 text-xs text-datumbim-text hover:bg-datumbim-border/50">
                Open Project
              </button>
              <button onClick={() => { setMenuOpen(false); executeCommand('file.import') }} className="w-full text-left px-3 py-1.5 text-xs text-datumbim-text hover:bg-datumbim-border/50">
                Import
              </button>
              <div className="border-t border-datumbim-border my-1" />
              <button onClick={handleSave} className="w-full text-left px-3 py-1.5 text-xs text-datumbim-text hover:bg-datumbim-border/50">
                Save
              </button>
              <button onClick={() => { setMenuOpen(false); addNotification({ type: 'info', message: 'Save As not yet implemented' }) }} className="w-full text-left px-3 py-1.5 text-xs text-datumbim-text hover:bg-datumbim-border/50">
                Save As
              </button>
              <div className="border-t border-datumbim-border my-1" />
              <button onClick={() => { setMenuOpen(false); addNotification({ type: 'info', message: 'Export not yet implemented' }) }} className="w-full text-left px-3 py-1.5 text-xs text-datumbim-text hover:bg-datumbim-border/50">
                Export
              </button>
            </div>
          )}
        </div>
        <button onClick={() => executeCommand('project.save')} className="text-xs text-datumbim-textSecondary hover:text-datumbim-text px-2 py-1 rounded hover:bg-datumbim-border/50">
          Save
        </button>
        <button onClick={() => addNotification({ type: 'info', message: 'Undo not yet implemented' })} className="text-xs text-datumbim-textSecondary hover:text-datumbim-text px-2 py-1 rounded hover:bg-datumbim-border/50">
          Undo
        </button>
        <button onClick={() => addNotification({ type: 'info', message: 'Redo not yet implemented' })} className="text-xs text-datumbim-textSecondary hover:text-datumbim-text px-2 py-1 rounded hover:bg-datumbim-border/50">
          Redo
        </button>
      </div>

      <div className="ml-auto flex items-center gap-3">
        {project.isOpen && project.name && (
          <span className="text-xs text-datumbim-textSecondary">
            {project.name}
            {project.isModified && <span className="ml-1 text-[10px] text-yellow-500">●</span>}
          </span>
        )}
        <span className="text-[11px] text-datumbim-textSecondary">TASK 006F — Real Frontend</span>
      </div>
    </div>
  )
}
