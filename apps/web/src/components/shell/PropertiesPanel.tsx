'use client'

import React, { useEffect, useMemo } from 'react'
import { useShellStore } from '@/store/shellStore'
import { useDesignSlice } from '@/store/slices/designSlice'
import { elementApi } from '@/lib/api/elements'

const PROPERTY_SCHEMAS = [
  {
    id: 'identity',
    label: 'Identity Data',
    properties: ['type_id', 'category', 'name'] as const,
  },
  {
    id: 'constraints',
    label: 'Constraints',
    properties: ['level_id', 'length', 'height', 'thickness'] as const,
  },
  {
    id: 'dimensions',
    label: 'Dimensions',
    properties: ['width', 'depth', 'area', 'volume'] as const,
  },
  {
    id: 'materials',
    label: 'Materials',
    properties: ['material', 'finish'] as const,
  },
  {
    id: 'location',
    label: 'Location',
    properties: ['x', 'y', 'z'] as const,
  },
  {
    id: 'graphics',
    label: 'Graphics',
    properties: ['visible', 'color', 'transparency'] as const,
  },
  {
    id: 'data',
    label: 'Data',
    properties: ['created_by', 'created_at', 'modified_at'] as const,
  },
]

function parseProperties(properties?: string) {
  if (!properties) return {}
  try {
    return JSON.parse(properties)
  } catch {
    return {}
  }
}

export default function PropertiesPanel() {
  const { addNotification, activeView } = useShellStore()
  const selectedIds = useDesignSlice((state) => state.getSelectedElements())
  const [elements, setElements] = React.useState<Record<string, { name: string; category: string; properties: Record<string, unknown> }>>({})

  useEffect(() => {
    let cancelled = false
    if (selectedIds.length === 0) {
      setElements({})
      return
    }
    ;(async () => {
      const results = await Promise.all(selectedIds.map((id) => elementApi.get(id)))
      if (cancelled) return
      const next: typeof elements = {}
      for (const res of results) {
        if (res.data) {
          next[res.data.id] = {
            name: res.data.name,
            category: res.data.category,
            properties: parseProperties(res.data.properties),
          }
        }
      }
      setElements(next)
    })()
    return () => {
      cancelled = true
    }
  }, [selectedIds])

  const selectedElement = useMemo(() => {
    const id = selectedIds[0]
    if (!id) return null
    return elements[id] || null
  }, [selectedIds, elements])

  const renderValue = (property: string) => {
    if (!selectedElement) return <span className="text-datumbim-textSecondary italic">Not set</span>
    const value = selectedElement.properties[property]
    if (value === undefined || value === null) {
      return <span className="text-datumbim-textSecondary italic">Not set</span>
    }
    if (typeof value === 'boolean') {
      return <span>{value ? 'Yes' : 'No'}</span>
    }
    const unit = property.toLowerCase().includes('area') ? ' m²' : property.toLowerCase().includes('length') || property.toLowerCase().includes('width') || property.toLowerCase().includes('height') ? ' mm' : ''
    return <span>{`${value}${unit}`}</span>
  }

  return (
    <div className="w-64 bg-datumbim-surface border-l border-datumbim-border flex flex-col h-full">
      <div className="h-8 border-b border-datumbim-border flex items-center justify-between px-3">
        <span className="text-[11px] font-semibold text-datumbim-textSecondary uppercase tracking-wider">
          Properties
        </span>
        <button
          onClick={() => addNotification({ type: 'info', message: 'Properties options' })}
          className="text-[10px] text-datumbim-textSecondary hover:text-datumbim-text"
        >
          ▼
        </button>
      </div>
      <div className="flex-1 overflow-auto p-3">
        {activeView ? (
          <div className="text-xs text-datumbim-textSecondary mb-3">
            View: {activeView.name}
          </div>
        ) : (
          <div className="text-xs text-datumbim-textSecondary mb-3">No selection</div>
        )}
        {selectedIds.length > 0 && (
          <div className="text-xs text-datumbim-textSecondary mb-3">
            {selectedIds.length} element{selectedIds.length !== 1 ? 's' : ''} selected
          </div>
        )}
        {selectedElement ? (
          <>
            <div className="mb-3">
              <div className="text-[11px] font-semibold text-datumbim-textSecondary mb-1 uppercase tracking-wider">Selected Element</div>
              <div className="text-xs text-datumbim-text">{selectedElement.name}</div>
              <div className="text-[11px] text-datumbim-textSecondary">{selectedElement.category}</div>
            </div>
            {PROPERTY_SCHEMAS.map((group) => {
              const relevant = group.properties.filter((key) => key in selectedElement.properties)
              if (relevant.length === 0) return null
              return (
                <div key={group.id} className="mb-4">
                  <div className="text-[11px] font-semibold text-datumbim-textSecondary mb-2 uppercase tracking-wider">
                    {group.label}
                  </div>
                  <div className="space-y-1">
                    {relevant.map((property) => (
                      <div key={property} className="flex items-center justify-between text-xs">
                        <span className="text-datumbim-textSecondary">{property}</span>
                        <span className="text-datumbim-text">{renderValue(property)}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )
            })}
          </>
        ) : (
          PROPERTY_SCHEMAS.map((group) => (
            <div key={group.id} className="mb-4">
              <div className="text-[11px] font-semibold text-datumbim-textSecondary mb-2 uppercase tracking-wider">
                {group.label}
              </div>
              <div className="space-y-1">
                {group.properties.map((property) => (
                  <div key={property} className="flex items-center justify-between text-xs">
                    <span className="text-datumbim-textSecondary">{property}</span>
                    <span className="text-datumbim-text">{renderValue(property)}</span>
                  </div>
                ))}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}
