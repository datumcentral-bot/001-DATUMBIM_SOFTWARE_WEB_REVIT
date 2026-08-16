import { create } from 'zustand'
import { ShellNotification, ShellDialog, ContextMenuState, ViewTab, ProjectState } from '@/types/shell'
import { DEFAULT_VIEW_TABS, RIBBON_TABS, RIBBON_PANELS } from '@/constants/shell'
import { CommandDefinition, ALL_COMMANDS } from '@/constants/commands'
import { CommandContext, CommandHistoryEntry, NavigationState, ViewDefinition } from '@/types/commands'
import { DESIGN_COMMAND_REGISTRY } from '@/commands'
import { projectApi } from '@/lib/api/projects'
import type { ProjectResponse } from '@/types/api'

interface ShellState {
  activeRibbonTab: string
  setActiveRibbonTab: (tab: string) => void
  ribbonTabs: typeof RIBBON_TABS
  ribbonPanels: typeof RIBBON_PANELS
  notifications: ShellNotification[]
  addNotification: (n: Omit<ShellNotification, 'id' | 'timestamp'>) => void
  removeNotification: (id: string) => void
  dialogs: ShellDialog[]
  openDialog: (d: Omit<ShellDialog, 'open'>) => void
  closeDialog: (id: string) => void
  contextMenu: ContextMenuState
  openContextMenu: (x: number, y: number, items: ContextMenuState['items']) => void
  closeContextMenu: () => void
  viewTabs: ViewTab[]
  activeViewTab: string | null
  setActiveViewTab: (id: string) => void
  commandPaletteOpen: boolean
  setCommandPaletteOpen: (open: boolean) => void
  navigationStack: string[]
  pushNavigation: (viewId: string) => void
  popNavigation: () => void
  commandRegistry: Map<string, CommandDefinition>
  registerCommand: (command: CommandDefinition) => void
  unregisterCommand: (id: string) => void
  executeCommand: (commandId: string) => Promise<void>
  commandHistory: CommandHistoryEntry[]
  undoCommand: () => Promise<void>
  redoCommand: () => Promise<void>
  commandContext: CommandContext
  updateCommandContext: (context: Partial<CommandContext>) => void
  navigation: NavigationState
  setNavigationMode: (mode: NavigationState['mode']) => void
  views: ViewDefinition[]
  activeView: ViewDefinition | null
  setActiveView: (viewId: string) => void
  project: ProjectState
  recentProjects: ProjectResponse[]
  projectLoading: boolean
  projectError: string | null
  openProject: (project: ProjectResponse) => void
  closeProject: () => void
  markProjectModified: () => void
  markProjectSaved: () => void
  loadRecentProjects: () => Promise<void>
  createProject: (payload: { name: string; description?: string }) => Promise<ProjectResponse | null>
}

export const useShellStore = create<ShellState>((set, get) => ({
  activeRibbonTab: 'architecture',
  setActiveRibbonTab: (tab) => set({ activeRibbonTab: tab }),
  ribbonTabs: RIBBON_TABS,
  ribbonPanels: RIBBON_PANELS,
  notifications: [],
  addNotification: (n) =>
    set((state) => ({
      notifications: [
        ...state.notifications,
        { ...n, id: crypto.randomUUID(), timestamp: new Date() },
      ],
    })),
  removeNotification: (id) =>
    set((state) => ({
      notifications: state.notifications.filter((n) => n.id !== id),
    })),
  dialogs: [],
  openDialog: (d) =>
    set((state) => ({
      dialogs: [...state.dialogs, { ...d, open: true }],
    })),
  closeDialog: (id) =>
    set((state) => ({
      dialogs: state.dialogs.map((d) => (d.id === id ? { ...d, open: false } : d)),
    })),
  contextMenu: { open: false, x: 0, y: 0, items: [] },
  openContextMenu: (x, y, items) =>
    set({ contextMenu: { open: true, x, y, items } }),
  closeContextMenu: () =>
    set((state) => ({ contextMenu: { ...state.contextMenu, open: false } })),
  viewTabs: DEFAULT_VIEW_TABS,
  activeViewTab: DEFAULT_VIEW_TABS[0]?.id ?? null,
  setActiveViewTab: (id) => set({ activeViewTab: id }),
  commandPaletteOpen: false,
  setCommandPaletteOpen: (open) => set({ commandPaletteOpen: open }),
  navigationStack: [],
  pushNavigation: (viewId) =>
    set((state) => ({ navigationStack: [...state.navigationStack, viewId] })),
  popNavigation: () =>
    set((state) => {
      const next = [...state.navigationStack]
      next.pop()
      return { navigationStack: next }
    }),
  commandRegistry: new Map([...ALL_COMMANDS, ...DESIGN_COMMAND_REGISTRY].map((cmd) => [cmd.id, cmd])),
  registerCommand: (command) =>
    set((state) => {
      const next = new Map(state.commandRegistry)
      next.set(command.id, command)
      return { commandRegistry: next }
    }),
  unregisterCommand: (id) =>
    set((state) => {
      const next = new Map(state.commandRegistry)
      next.delete(id)
      return { commandRegistry: next }
    }),
  executeCommand: async (commandId, ...args: unknown[]) => {
    const cmd = get().commandRegistry.get(commandId)
    if (!cmd) {
      get().addNotification({ type: 'warning', message: `Unknown command: ${commandId}` })
      return
    }
    if (!cmd.enabled) {
      get().addNotification({ type: 'warning', message: `Command disabled: ${cmd.label}` })
      return
    }
    const context = get().commandContext
    const result = await (cmd as { handler?: (command: typeof cmd, ...handlerArgs: unknown[]) => Promise<{ success: boolean; message?: string }> }).handler?.(cmd, context, ...args)
    const message = result?.message ?? `Command executed: ${cmd.label}`
    const success = result?.success ?? true
    get().addNotification({ type: success ? 'info' : 'error', message })
    const entry: CommandHistoryEntry = {
      commandId: cmd.id,
      timestamp: Date.now(),
      context: get().commandContext,
      result: success ? 'success' : 'failure',
    }
    set((state) => ({ commandHistory: [...state.commandHistory, entry] }))
  },
  commandHistory: [],
  undoCommand: async () => {
    const history = get().commandHistory
    if (history.length === 0) return
    const last = history[history.length - 1]
    set((state) => ({
      commandHistory: state.commandHistory.slice(0, -1),
    }))
    get().addNotification({ type: 'info', message: `Undo: ${last.commandId}` })
  },
  redoCommand: async () => {
    get().addNotification({ type: 'info', message: 'Redo not yet implemented' })
  },
  commandContext: {
    selectionIds: [],
    viewId: null,
    projectId: null,
    permissions: [],
    engine: 'none',
  },
  updateCommandContext: (context) =>
    set((state) => ({ commandContext: { ...state.commandContext, ...context } })),
  navigation: { mode: 'pan', status: 'available' },
  setNavigationMode: (mode) => set({ navigation: { mode, status: 'available' } }),
  views: [
    { id: 'view-3d', name: '{3D}', type: '3d', discipline: 'generic', visibilityState: true, activeState: true },
    { id: 'floor-plan', name: 'Floor Plan', type: 'floor-plan', discipline: 'architecture', visibilityState: true, activeState: false },
    { id: 'ceiling-plan', name: 'Ceiling Plan', type: 'ceiling-plan', discipline: 'architecture', visibilityState: true, activeState: false },
    { id: 'elevation-1', name: 'Elevation 1', type: 'elevation', discipline: 'architecture', visibilityState: true, activeState: false },
    { id: 'section-1', name: 'Section 1', type: 'section', discipline: 'architecture', visibilityState: true, activeState: false },
    { id: 'control', name: 'Control', type: 'control', discipline: 'generic', visibilityState: true, activeState: false },
  ],
  activeView: null,
  setActiveView: (viewId) => {
    const view = get().views.find((v) => v.id === viewId) || null
    set({ activeView: view })
  },
  project: {
    id: null,
    name: null,
    description: null,
    isOpen: false,
    isModified: false,
    lastSavedAt: null,
  },
  recentProjects: [],
  projectLoading: false,
  projectError: null,
  openProject: async (project) => {
    set({ projectLoading: true, projectError: null })
    try {
      const res = await projectApi.open(project.id)
      if (res.error) {
        set({ projectError: res.error, projectLoading: false })
        return
      }
      set({
        project: {
          id: project.id,
          name: project.name,
          description: project.description ?? null,
          isOpen: true,
          isModified: false,
          lastSavedAt: new Date(),
        },
        projectLoading: false,
      })
      get().loadRecentProjects()
    } catch (e) {
      set({ projectError: e instanceof Error ? e.message : 'Failed to open project', projectLoading: false })
    }
  },
  closeProject: () => {
    set({
      project: {
        id: null,
        name: null,
        description: null,
        isOpen: false,
        isModified: false,
        lastSavedAt: null,
      },
    })
  },
  markProjectModified: () =>
    set((state) => ({
      project: { ...state.project, isModified: true },
    })),
  markProjectSaved: () =>
    set((state) => ({
      project: { ...state.project, isModified: false, lastSavedAt: new Date() },
    })),
  loadRecentProjects: async () => {
    const res = await projectApi.list()
    if (!res.error && res.data) {
      set({ recentProjects: res.data as ProjectResponse[] })
    }
  },
  createProject: async (payload) => {
    set({ projectLoading: true, projectError: null })
    try {
      const res = await projectApi.create(payload)
      if (res.error || !res.data) {
        set({ projectError: res.error || 'Failed to create project', projectLoading: false })
        return null
      }
      const created = res.data as ProjectResponse
      set({
        project: {
          id: created.id,
          name: created.name,
          description: created.description ?? null,
          isOpen: true,
          isModified: false,
          lastSavedAt: new Date(),
        },
        projectLoading: false,
      })
      get().loadRecentProjects()
      return created
    } catch (e) {
      set({ projectError: e instanceof Error ? e.message : 'Failed to create project', projectLoading: false })
      return null
    }
  },
}))
