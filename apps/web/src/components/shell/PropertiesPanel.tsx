'use client'

import React from 'react'
import { useShellStore } from '@/store/shellStore'
import { PropertyGroup } from '@/types/commands'
import { useDesignSlice } from '@/store/slices/designSlice'

const PROPERTY_SCHEMAS: PropertyGroup[] = [
  {
    id: 'identity',
    label: 'Identity Data',
    properties: [
      { key: 'mark', label: 'Mark', type: 'text', value: '—' },
      { key: 'type', label: 'Type', type: 'text', value: '—' },
      { key: 'level', label: 'Level', type: 'text', value: '—' },
    ],
  },
  {
    id: 'constraints',
    label: 'Constraints',
    properties: [
      { key: 'base-level', label: 'Base Level', type: 'text', value: '—' },
      { key: 'top-level', label: 'Top Level', type: 'text', value: '—' },
      { key: 'height', label: 'Height', type: 'length', value: null, unit: 'mm' },
    ],
  },
  {
    id: 'dimensions',
    label: 'Dimensions',
    properties: [
      { key: 'width', label: 'Width', type: 'length', value: null, unit: 'mm' },
      { key: 'depth', label: 'Depth', type: 'length', value: null, unit: 'mm' },
      { key: 'area', label: 'Area', type: 'area', value: null, unit: 'm²' },
    ],
  },
  {
    id: 'materials',
    label: 'Materials',
    properties: [
      { key: 'material', label: 'Material', type: 'material', value: '—' },
      { key: 'finish', label: 'Finish', type: 'text', value: '—' },
    ],
  },
  {
    id: 'location',
    label: 'Location',
    properties: [
      { key: 'x', label: 'X', type: 'length', value: null, unit: 'mm' },
      { key: 'y', label: 'Y', type: 'length', value: null, unit: 'mm' },
      { key: 'z', label: 'Z', type: 'length', value: null, unit: 'mm' },
    ],
  },
  {
    id: 'graphics',
    label: 'Graphics',
    properties: [
      { key: 'visible', label: 'Visible', type: 'boolean', value: true },
      { key: 'color', label: 'Color', type: 'text', value: '—' },
      { key: 'transparency', label: 'Transparency', type: 'number', value: 0, unit: '%' },
    ],
  },
  {
    id: 'data',
    label: 'Data',
    properties: [
      { key: 'created-by', label: 'Created By', type: 'text', value: '—' },
      { key: 'created-at', label: 'Created At', type: 'text', value: '—' },
      { key: 'modified-at', label: 'Modified At', type: 'text', value: '—' },
    ],
  },
]

export default function PropertiesPanel() {
  const { addNotification, activeView } = useShellStore()
  const selectedIds = useDesignSlice((state) => state.getSelectedElements())
  const hasSelection = selectedIds.length > 0

  const renderValue = (property: PropertyGroup['properties'][number]) => {
    if (property.value === null || property.value === undefined) {
      return <span className="text-datumbim-textSecondary italic">Not set</span>
    }
    if (property.type === 'boolean') {
      return <span>{property.value ? 'Yes' : 'No'}</span>
    }
    const display = `${property.value}${property.unit ? ` ${property.unit}` : ''}`
    return <span>{display}</span>
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
        {hasSelection && (
          <div className="text-xs text-datumbim-textSecondary mb-3">
            {selectedIds.length} element{selectedIds.length !== 1 ? 's' : ''} selected
          </div>
        )}
        {PROPERTY_SCHEMAS.map((group) => (
          <div key={group.id} className="mb-4">
            <div className="text-[11px] font-semibold text-datumbim-textSecondary mb-2 uppercase tracking-wider">
              {group.label}
            </div>
            <div className="space-y-1">
              {group.properties.map((property) => (
                <div key={property.key} className="flex items-center justify-between text-xs">
                  <span className="text-datumbim-textSecondary">{property.label}</span>
                  <span className="text-datumbim-text">{renderValue(property)}</span>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
