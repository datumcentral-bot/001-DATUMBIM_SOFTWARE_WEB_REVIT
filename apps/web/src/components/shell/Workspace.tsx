'use client'

import React, { useEffect } from 'react'
import ViewTabs from './ViewTabs'
import NavigationBreadcrumb from './NavigationBreadcrumb'
import Canvas from './Canvas'
import NavigationControls from './NavigationControls'
import ApplicationsScreen from '@/components/connectors/ApplicationsScreen'
import SessionsScreen from '@/components/connectors/SessionsScreen'
import ObservationScreen from '@/components/connectors/ObservationScreen'
import ControlScreen from '@/components/control/ControlScreen'
import LiveApplicationScreen from '@/components/observation/LiveApplicationScreen'
import IntegrationsScreen from '@/components/integrations/IntegrationsScreen'
import { useShellStore } from '@/store/shellStore'
import { useDesignSlice } from '@/store/slices/designSlice'

export default function Workspace() {
  const { addNotification, views, setActiveView, activeView } = useShellStore()
  const initialize = useDesignSlice((state) => state.initialize)
  const viewType = activeView?.type || '3d'

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
        {viewType === 'applications' ? (
          <ApplicationsScreen />
        ) : viewType === 'sessions' ? (
          <SessionsScreen />
        ) : viewType === 'observation' ? (
          <ObservationScreen />
        ) : viewType === 'control' ? (
          <ControlScreen />
        ) : viewType === 'live-application' ? (
          <LiveApplicationScreen />
        ) : viewType === 'integrations' ? (
          <IntegrationsScreen />
        ) : (
          <>
            <Canvas />
            <NavigationControls />
          </>
        )}
      </div>
    </div>
  )
}
