'use client'

import React from 'react'
import TopBar from './TopBar'
import QuickAccessToolbar from './QuickAccessToolbar'
import Ribbon from './Ribbon'
import ProjectBrowser from './ProjectBrowser'
import PropertiesPanel from './PropertiesPanel'
import Workspace from './Workspace'
import StatusBar from './StatusBar'
import Notifications from './Notifications'
import Search from './Search'
import CommandLauncher from './CommandLauncher'
import Dialog from './Dialog'
import ContextMenu from './ContextMenu'
import NavigationBreadcrumb from './NavigationBreadcrumb'
import KeyboardShortcutsHelp from './KeyboardShortcutsHelp'

export default function AppShell() {
  return (
    <div className="h-screen w-screen flex flex-col bg-datumbim-bg text-datumbim-text overflow-hidden">
      <TopBar />
      <QuickAccessToolbar />
      <Ribbon />
      <div className="flex-1 flex overflow-hidden">
        <ProjectBrowser />
        <Workspace />
        <PropertiesPanel />
      </div>
      <StatusBar />
      <NavigationBreadcrumb />
      <Notifications />
      <Search />
      <CommandLauncher />
      <Dialog />
      <ContextMenu />
      <KeyboardShortcutsHelp />
    </div>
  )
}
