'use client'

import React, { useEffect, useRef } from 'react'
import { useShellStore } from '@/store/shellStore'

export default function ContextMenu() {
  const { contextMenu, closeContextMenu } = useShellStore()
  const menuRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(e.target as Node)) {
        closeContextMenu()
      }
    }
    if (contextMenu.open) {
      document.addEventListener('mousedown', handleClickOutside)
    }
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [contextMenu.open, closeContextMenu])

  if (!contextMenu.open) return null

  return (
    <div
      ref={menuRef}
      className="fixed z-50 bg-datumbim-surface border border-datumbim-border rounded shadow-xl py-1 min-w-[180px]"
      style={{ left: contextMenu.x, top: contextMenu.y }}
    >
      {contextMenu.items.map((item) =>
        item.divider ? (
          <div key={item.id} className="h-px bg-datumbim-border my-1" />
        ) : (
          <button
            key={item.id}
            disabled={item.disabled}
            className={`w-full flex items-center gap-2 px-3 py-1.5 text-xs text-left ${
              item.disabled ? 'opacity-40 cursor-not-allowed' : 'hover:bg-datumbim-border/50 text-datumbim-text'
            }`}
          >
            {item.icon && <span>{item.icon}</span>}
            <span>{item.label}</span>
          </button>
        )
      )}
    </div>
  )
}
