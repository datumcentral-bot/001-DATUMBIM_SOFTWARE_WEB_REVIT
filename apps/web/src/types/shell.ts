export interface RibbonTab {
  id: string
  label: string
  panels: RibbonPanel[]
}

export interface RibbonPanel {
  id: string
  label: string
  items: RibbonItem[]
}

export interface RibbonItem {
  id: string
  type: 'button' | 'split' | 'toggle'
  label: string
  icon?: string
  command?: string
  disabled?: boolean
}

export interface ViewTab {
  id: string
  label: string
  type: '3d' | 'floor-plan' | 'ceiling-plan' | 'elevation' | 'section' | 'detail' | 'schedule' | 'sheet' | 'drafting' | 'browser' | 'model' | 'applications' | 'sessions' | 'observation' | 'control' | 'ai' | 'planner'
  active?: boolean
}

export interface ShellNotification {
  id: string
  type: 'info' | 'success' | 'warning' | 'error'
  message: string
  timestamp: Date
}

export interface ShellDialog {
  id: string
  title: string
  content?: React.ReactNode
  open: boolean
}

export interface ContextMenuState {
  open: boolean
  x: number
  y: number
  items: ContextMenuItem[]
}

export interface ContextMenuItem {
  id: string
  label: string
  icon?: string
  disabled?: boolean
  divider?: boolean
  action?: string
  shortcut?: string
}

export interface NavigationState {
  stack: string[]
  currentView: string | null
}

export interface ProjectState {
  id: string | null
  name: string | null
  description: string | null
  isOpen: boolean
  isModified: boolean
  lastSavedAt: Date | null
}
