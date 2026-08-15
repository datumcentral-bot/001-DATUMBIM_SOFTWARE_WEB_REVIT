'use client'

import React, { useEffect } from 'react'
import ViewTabs from './ViewTabs'
import NavigationBreadcrumb from './NavigationBreadcrumb'
import Canvas from './Canvas'
import NavigationControls from './NavigationControls'
import { useShellStore } from '@/store/shellStore'
import { useDesignSlice } from '@/store/slices/designSlice'

export default function Workspace() {
  const { addNotification } = useShellStore()
  const initialize = useDesignSlice((state) => state.initialize)

  useEffect(() => {
    initialize()
    addNotification({ type: 'info', message: 'Design engine initialized' })
  }, [initialize, addNotification])

  return (
    <div className="flex-1 flex flex-col min-w-0 bg-datumbim-bg">
      <NavigationBreadcrumb />
      <ViewTabs />
      <div className="flex-1 relative">
        <Canvas />
        <NavigationControls />
      </div>
    </div>
  )
}
