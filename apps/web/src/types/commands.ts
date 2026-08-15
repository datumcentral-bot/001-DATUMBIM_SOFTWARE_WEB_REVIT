export type CommandState = 'idle' | 'active' | 'disabled' | 'hidden' | 'placeholder'

export interface CommandContext {
  selectionIds: string[]
  viewId: string | null
  projectId: string | null
  permissions: string[]
  engine: 'revit' | 'autocad' | 'navisworks' | 'ifc' | 'none'
}

export interface CommandHistoryEntry {
  commandId: string
  timestamp: number
  context: CommandContext
  result: 'success' | 'failure' | 'cancelled'
}

export interface CommandHandlerResult {
  success: boolean
  message?: string
  data?: unknown
}

export type CommandHandler = (command: CommandDefinition, context: CommandContext) => Promise<CommandHandlerResult> | CommandHandlerResult

export interface CommandDefinition {
  id: string
  name: string
  label: string
  description?: string
  icon?: string
  category: CommandCategory['id']
  tab: string
  panel: string
  shortcut?: string
  enabled: boolean
  visible: boolean
  availability: string[]
  commandType: 'button' | 'split' | 'toggle' | 'menu'
  implementationTarget: string
  placeholder?: boolean
  action: string
}

export interface CommandCategory {
  id: string
  label: string
  commands: CommandDefinition[]
}

export interface ViewDefinition {
  id: string
  name: string
  type: '3d' | 'floor-plan' | 'ceiling-plan' | 'elevation' | 'section' | 'detail' | 'schedule' | 'sheet' | 'drafting' | 'browser' | 'model'
  discipline: 'architecture' | 'structure' | 'mep' | 'coordination' | 'generic'
  visibilityState: boolean
  activeState: boolean
  cameraState?: {
    position: { x: number; y: number; z: number }
    target: { x: number; y: number; z: number }
    up: { x: number; y: number; z: number }
  }
  modelReference?: string
}

export interface PropertyGroup {
  id: string
  label: string
  properties: PropertyDefinition[]
}

export interface PropertyDefinition {
  key: string
  label: string
  type: 'text' | 'number' | 'boolean' | 'enum' | 'length' | 'area' | 'volume' | 'material' | 'element'
  value: unknown
  readonly?: boolean
  unit?: string
}

export interface NavigationState {
  mode: 'pan' | 'zoom' | 'orbit' | 'walk' | 'fit' | 'select' | 'window-select' | 'crossing-select' | 'view-cube' | 'navigation-wheel'
  status: 'available' | 'coming-soon' | 'requires-viewer' | 'requires-model' | 'requires-service'
}
