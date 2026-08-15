'use client'

import React, { useEffect } from 'react'
import ViewTabs from './ViewTabs'
import NavigationBreadcrumb from './NavigationBreadcrumb'
import Canvas from './Canvas'
import NavigationControls from './NavigationControls'
import { useShellStore } from '@/store/shellStore'
import { useDesignSlice } from '@/store/slices/designSlice'

export default function Workspace() {
  const { addNotification, views, setActiveView } = useShellStore()
  const initialize = useDesignSlice((state) => state.initialize)

  useEffect(() => {
    initialize()
    addNotification({ type: 'info', message: 'DATUMBIM Workspace ready' })
  }, [initialize, addNotification])

  const handleViewChange = (viewId: string) => {
    const view = views.find((v) => v.id === viewId)
    if (view) {
      setActiveView(viewId)
      addNotification({ type: 'info', message: `Switched to: ${view.name}` })
    }
  }

  return (
    <div className="flex-1 flex flex-col min-w-0 bg-datumbim-bg">
      <NavigationBreadcrumb />
      <ViewTabs activeTab={useShellStore.getState().activeViewTab || views[0]?.id || null} onTabChange={handleViewChange} />
      <div className="flex-1 relative">
        <Canvas />
        <NavigationControls />
      </div>
    </div>
  )
}
