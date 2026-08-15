'use client'

import React, { useEffect, useMemo, useState } from 'react'
import { useShellStore } from '@/store/shellStore'
import { useDesignSlice } from '@/store/slices/designSlice'
import { elementApi } from '@/lib/api/elements'
import type { ElementResponse } from '@/types/api'

type PropertyGroup = {
  id: string
  label: string
  icon: string
  properties: Array<{ key: string; label: string; unit?: string }>
}

const ELEMENT_PROPERTY_SCHEMAS: Record<string, PropertyGroup[]> = {
  wall: [
    {
      id: 'identity',
      label: 'Identity',
      icon: '🏷️',
      properties: [
        { key: 'name', label: 'Name' },
        { key: 'type_id', label: 'Type' },
        { key: 'category', label: 'Category' },
      ],
    },
    {
      id: 'dimensions',
      label: 'Dimensions',
      icon: '📐',
      properties: [
        { key: 'length', label: 'Length', unit: 'mm' },
        { key: 'height', label: 'Height', unit: 'mm' },
        { key: 'thickness', label: 'Thickness', unit: 'mm' },
        { key: 'area', label: 'Area', unit: 'm²' },
        { key: 'volume', label: 'Volume', unit: 'm³' },
      ],
    },
    {
      id: 'location',
      label: 'Location',
      icon: '📍',
      properties: [
        { key: 'level_id', label: 'Level' },
        { key: 'base_level', label: 'Base Level' },
      ],
    },
    {
      id: 'graphics',
      label: 'Graphics',
      icon: '🎨',
      properties: [
        { key: 'visible', label: 'Visible' },
      ],
    },
  ],
  door: [
    {
      id: 'identity',
      label: 'Identity',
      icon: '🏷️',
      properties: [
        { key: 'name', label: 'Name' },
        { key: 'type_id', label: 'Type' },
        { key: 'category', label: 'Category' },
      ],
    },
    {
      id: 'dimensions',
      label: 'Dimensions',
      icon: '📐',
      properties: [
        { key: 'width', label: 'Width', unit: 'mm' },
        { key: 'height', label: 'Height', unit: 'mm' },
        { key: 'sill_height', label: 'Sill Height', unit: 'mm' },
        { key: 'head_height', label: 'Head Height', unit: 'mm' },
      ],
    },
    {
      id: 'location',
      label: 'Location',
      icon: '📍',
      properties: [
        { key: 'level_id', label: 'Level' },
      ],
    },
  ],
  window: [
    {
      id: 'identity',
      label: 'Identity',
      icon: '🏷️',
      properties: [
        { key: 'name', label: 'Name' },
        { key: 'type_id', label: 'Type' },
        { key: 'category', label: 'Category' },
      ],
    },
    {
      id: 'dimensions',
      label: 'Dimensions',
      icon: '📐',
      properties: [
        { key: 'width', label: 'Width', unit: 'mm' },
        { key: 'height', label: 'Height', unit: 'mm' },
        { key: 'sill_height', label: 'Sill Height', unit: 'mm' },
        { key: 'head_height', label: 'Head Height', unit: 'mm' },
      ],
    },
    {
      id: 'location',
      label: 'Location',
      icon: '📍',
      properties: [
        { key: 'level_id', label: 'Level' },
      ],
    },
  ],
  default: [
    {
      id: 'identity',
      label: 'Identity',
      icon: '🏷️',
      properties: [
        { key: 'name', label: 'Name' },
        { key: 'type_id', label: 'Type' },
        { key: 'category', label: 'Category' },
      ],
    },
    {
      id: 'dimensions',
      label: 'Dimensions',
      icon: '📐',
      properties: [
        { key: 'length', label: 'Length', unit: 'mm' },
        { key: 'area', label: 'Area', unit: 'm²' },
      ],
    },
    {
      id: 'graphics',
      label: 'Graphics',
      icon: '🎨',
      properties: [
        { key: 'visible', label: 'Visible' },
      ],
    },
  ],
}

function getCategory(element: ElementResponse): string {
  const cat = element.category.toLowerCase()
  if (cat.includes('wall')) return 'wall'
  if (cat.includes('door')) return 'door'
  if (cat.includes('window')) return 'window'
  if (cat.includes('roof')) return 'roof'
  if (cat.includes('floor')) return 'floor'
  if (cat.includes('column')) return 'column'
  if (cat.includes('beam')) return 'beam'
  if (cat.includes('duct')) return 'duct'
  if (cat.includes('pipe')) return 'pipe'
  return 'default'
}

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
  const viewerEngine = useDesignSlice((state) => state.getViewerEngine())
  const [elements, setElements] = useState<Record<string, ElementResponse>>({})

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
          next[res.data.id] = res.data
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
    const apiElement = elements[id] || null
    const viewerMetadata = viewerEngine?.getBIMElementMetadata(id)
    if (viewerMetadata) {
      return {
        id: viewerMetadata.id as string,
        name: viewerMetadata.name as string,
        category: viewerMetadata.category as string,
        properties: viewerMetadata.metadata as Record<string, unknown>,
      } as unknown as ElementResponse
    }
    return apiElement
  }, [selectedIds, elements, viewerEngine])

  const propertyGroups = useMemo(() => {
    if (!selectedElement) return []
    const category = getCategory(selectedElement)
    return ELEMENT_PROPERTY_SCHEMAS[category] || ELEMENT_PROPERTY_SCHEMAS.default
  }, [selectedElement])

  const renderValue = (property: string, unit?: string) => {
    if (!selectedElement) return <span className="text-datumbim-textSecondary italic">Not set</span>
    const value = parseProperties(selectedElement.properties)[property] ?? (selectedElement as unknown as Record<string, unknown>)[property]
    if (value === undefined || value === null || value === '') {
      return <span className="text-datumbim-textSecondary italic">Not set</span>
    }
    if (typeof value === 'boolean') {
      return <span>{value ? 'Yes' : 'No'}</span>
    }
    return <span>{`${value}${unit ? ` ${unit}` : ''}`}</span>
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
            View: <span className="text-datumbim-text">{activeView.name}</span>
          </div>
        ) : (
          <div className="text-xs text-datumbim-textSecondary mb-3">No active view</div>
        )}
        {selectedIds.length > 0 && (
          <div className="text-xs text-datumbim-textSecondary mb-3">
            {selectedIds.length} element{selectedIds.length !== 1 ? 's' : ''} selected
          </div>
        )}
        {selectedElement ? (
          <>
            <div className="mb-4 pb-3 border-b border-datumbim-border">
              <div className="text-xs font-semibold text-datumbim-text mb-1">{selectedElement.name}</div>
              <div className="text-[11px] text-datumbim-textSecondary">{selectedElement.category}</div>
              <div className="text-[10px] text-datumbim-textSecondary mt-1 font-mono">ID: {selectedElement.id}</div>
            </div>
            {propertyGroups.map((group) => (
              <div key={group.id} className="mb-4">
                <div className="text-[11px] font-semibold text-datumbim-textSecondary mb-2 uppercase tracking-wider flex items-center gap-1">
                  <span>{group.icon}</span>
                  {group.label}
                </div>
                <div className="space-y-1.5">
                  {group.properties.map((property) => (
                    <div key={property.key} className="flex items-center justify-between text-xs">
                      <span className="text-datumbim-textSecondary">{property.label}</span>
                      <span className="text-datumbim-text text-right">{renderValue(property.key, property.unit)}</span>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </>
        ) : (
          <div className="text-xs text-datumbim-textSecondary italic">No element selected</div>
        )}
      </div>
    </div>
  )
}
