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

export const COMMAND_CATEGORIES: CommandCategory[] = [
  {
    id: 'file',
    label: 'File',
    commands: [
      { id: 'new-project', name: 'new-project', label: 'New Project', shortcut: 'Ctrl+N', category: 'file', tab: 'datumbim', panel: 'core', commandType: 'button', implementationTarget: 'TASK 006', action: 'project.create', enabled: true, visible: true, availability: ['always'] },
      { id: 'open', name: 'open', label: 'Open', shortcut: 'Ctrl+O', category: 'file', tab: 'datumbim', panel: 'core', commandType: 'button', implementationTarget: 'TASK 006', action: 'file.open', enabled: true, visible: true, availability: ['always'] },
      { id: 'save', name: 'save', label: 'Save', shortcut: 'Ctrl+S', category: 'file', tab: 'datumbim', panel: 'core', commandType: 'button', implementationTarget: 'TASK 006', action: 'file.save', enabled: true, visible: true, availability: ['project-open'] },
      { id: 'save-as', name: 'save-as', label: 'Save As', shortcut: 'Ctrl+Shift+S', category: 'file', tab: 'datumbim', panel: 'core', commandType: 'button', implementationTarget: 'TASK 006', action: 'file.saveAs', enabled: true, visible: true, availability: ['project-open'] },
      { id: 'export', name: 'export', label: 'Export', shortcut: 'Ctrl+E', category: 'file', tab: 'datumbim', panel: 'core', commandType: 'button', implementationTarget: 'TASK 014', action: 'file.export', enabled: true, visible: true, availability: ['project-open'] },
      { id: 'print', name: 'print', label: 'Print', shortcut: 'Ctrl+P', category: 'file', tab: 'datumbim', panel: 'core', commandType: 'button', implementationTarget: 'TASK 014', action: 'file.print', enabled: true, visible: true, availability: ['project-open'] },
    ],
  },
  {
    id: 'edit',
    label: 'Edit',
    commands: [
      { id: 'undo', name: 'undo', label: 'Undo', shortcut: 'Ctrl+Z', category: 'edit', tab: 'datumbim', panel: 'core', commandType: 'button', implementationTarget: 'TASK 005', action: 'edit.undo', enabled: true, visible: true, availability: ['history-available'] },
      { id: 'redo', name: 'redo', label: 'Redo', shortcut: 'Ctrl+Y', category: 'edit', tab: 'datumbim', panel: 'core', commandType: 'button', implementationTarget: 'TASK 005', action: 'edit.redo', enabled: true, visible: true, availability: ['history-available'] },
      { id: 'cut', name: 'cut', label: 'Cut', shortcut: 'Ctrl+X', category: 'edit', tab: 'datumbim', panel: 'core', commandType: 'button', implementationTarget: 'TASK 005', action: 'edit.cut', enabled: true, visible: true, availability: ['selection-exists'] },
      { id: 'copy', name: 'copy', label: 'Copy', shortcut: 'Ctrl+C', category: 'edit', tab: 'datumbim', panel: 'core', commandType: 'button', implementationTarget: 'TASK 005', action: 'edit.copy', enabled: true, visible: true, availability: ['selection-exists'] },
      { id: 'paste', name: 'paste', label: 'Paste', shortcut: 'Ctrl+V', category: 'edit', tab: 'datumbim', panel: 'core', commandType: 'button', implementationTarget: 'TASK 005', action: 'edit.paste', enabled: true, visible: true, availability: ['clipboard-has-data'] },
      { id: 'delete', name: 'delete', label: 'Delete', shortcut: 'Del', category: 'edit', tab: 'datumbim', panel: 'core', commandType: 'button', implementationTarget: 'TASK 005', action: 'edit.delete', enabled: true, visible: true, availability: ['selection-exists'] },
      { id: 'select-all', name: 'select-all', label: 'Select All', shortcut: 'Ctrl+A', category: 'edit', tab: 'datumbim', panel: 'core', commandType: 'button', implementationTarget: 'TASK 005', action: 'selection.all', enabled: true, visible: true, availability: ['model-loaded'] },
    ],
  },
  {
    id: 'view',
    label: 'View',
    commands: [
      { id: 'zoom-extents', name: 'zoom-extents', label: 'Zoom Extents', shortcut: 'Ctrl+E', category: 'view', tab: 'view', panel: 'navigation', commandType: 'button', implementationTarget: 'TASK 003', action: 'view.zoomExtents', enabled: true, visible: true, availability: ['view-active'] },
      { id: 'zoom-in', name: 'zoom-in', label: 'Zoom In', shortcut: 'Ctrl+=', category: 'view', tab: 'view', panel: 'navigation', commandType: 'button', implementationTarget: 'TASK 003', action: 'view.zoomIn', enabled: true, visible: true, availability: ['view-active'] },
      { id: 'zoom-out', name: 'zoom-out', label: 'Zoom Out', shortcut: 'Ctrl+-', category: 'view', tab: 'view', panel: 'navigation', commandType: 'button', implementationTarget: 'TASK 003', action: 'view.zoomOut', enabled: true, visible: true, availability: ['view-active'] },
      { id: 'pan', name: 'pan', label: 'Pan', shortcut: 'Ctrl+P', category: 'view', tab: 'view', panel: 'navigation', commandType: 'toggle', implementationTarget: 'TASK 003', action: 'view.pan', enabled: true, visible: true, availability: ['view-active'] },
      { id: 'orbit', name: 'orbit', label: 'Orbit', shortcut: 'Ctrl+O', category: 'view', tab: 'view', panel: 'navigation', commandType: 'toggle', implementationTarget: 'TASK 003', action: 'view.orbit', enabled: true, visible: true, availability: ['view-active', '3d-view'] },
      { id: 'walk', name: 'walk', label: 'Walk', shortcut: 'Ctrl+W', category: 'view', tab: 'view', panel: 'navigation', commandType: 'toggle', implementationTarget: 'TASK 003', action: 'view.walk', enabled: true, visible: true, availability: ['view-active', '3d-view'] },
      { id: 'fit', name: 'fit', label: 'Fit to View', shortcut: 'Ctrl+Shift+F', category: 'view', tab: 'view', panel: 'navigation', commandType: 'button', implementationTarget: 'TASK 003', action: 'view.fit', enabled: true, visible: true, availability: ['view-active', 'selection-exists'] },
    ],
  },
  {
    id: 'navigate',
    label: 'Navigate',
    commands: [
      { id: 'go-to-level', name: 'go-to-level', label: 'Go to Level', shortcut: 'Ctrl+G', category: 'navigate', tab: 'view', panel: 'navigation', commandType: 'button', implementationTarget: 'TASK 004', action: 'nav.level', enabled: true, visible: true, availability: ['view-active'] },
      { id: 'go-to-view', name: 'go-to-view', label: 'Go to View', shortcut: 'Ctrl+Shift+G', category: 'navigate', tab: 'view', panel: 'navigation', commandType: 'button', implementationTarget: 'TASK 004', action: 'nav.view', enabled: true, visible: true, availability: ['view-active'] },
      { id: 'previous-view', name: 'previous-view', label: 'Previous View', shortcut: 'Alt+Left', category: 'navigate', tab: 'view', panel: 'history', commandType: 'button', implementationTarget: 'TASK 003', action: 'nav.previous', enabled: true, visible: true, availability: ['navigation-history'] },
      { id: 'next-view', name: 'next-view', label: 'Next View', shortcut: 'Alt+Right', category: 'navigate', tab: 'view', panel: 'history', commandType: 'button', implementationTarget: 'TASK 003', action: 'nav.next', enabled: true, visible: true, availability: ['navigation-history'] },
    ],
  },
  {
    id: 'automate',
    label: 'Automate',
    commands: [
      { id: 'design-automation', name: 'design-automation', label: 'Design Automation', shortcut: 'Ctrl+Shift+D', category: 'automate', tab: 'automate', panel: 'automation', commandType: 'button', implementationTarget: 'TASK 011', action: 'automation.design', enabled: true, visible: true, availability: ['always'], placeholder: true },
      { id: 'automation-jobs', name: 'automation-jobs', label: 'Automation Jobs', shortcut: 'Ctrl+Shift+J', category: 'automate', tab: 'automate', panel: 'automation', commandType: 'button', implementationTarget: 'TASK 011', action: 'automation.jobs', enabled: true, visible: true, availability: ['always'], placeholder: true },
      { id: 'batch-processing', name: 'batch-processing', label: 'Batch Processing', shortcut: 'Ctrl+Shift+B', category: 'automate', tab: 'automate', panel: 'automation', commandType: 'button', implementationTarget: 'TASK 011', action: 'automation.batch', enabled: true, visible: true, availability: ['always'], placeholder: true },
      { id: 'scripts', name: 'scripts', label: 'Scripts', shortcut: 'Ctrl+Shift+S', category: 'automate', tab: 'automate', panel: 'scripts', commandType: 'button', implementationTarget: 'TASK 011', action: 'automation.scripts', enabled: true, visible: true, availability: ['always'], placeholder: true },
      { id: 'addins', name: 'addins', label: 'Add-ins', shortcut: 'Ctrl+Shift+A', category: 'automate', tab: 'automate', panel: 'plugins', commandType: 'button', implementationTarget: 'TASK 013', action: 'automation.addins', enabled: true, visible: true, availability: ['always'], placeholder: true },
      { id: 'plugins', name: 'plugins', label: 'Plugins', shortcut: 'Ctrl+Shift+P', category: 'automate', tab: 'automate', panel: 'plugins', commandType: 'button', implementationTarget: 'TASK 013', action: 'automation.plugins', enabled: true, visible: true, availability: ['always'], placeholder: true },
      { id: 'job-monitor', name: 'job-monitor', label: 'Job Monitor', shortcut: 'Ctrl+Shift+M', category: 'automate', tab: 'automate', panel: 'monitor', commandType: 'button', implementationTarget: 'TASK 011', action: 'automation.monitor', enabled: true, visible: true, availability: ['always'], placeholder: true },
    ],
  },
  {
    id: 'aps',
    label: 'APS',
    commands: [
      { id: 'aps-viewer', name: 'aps-viewer', label: 'APS Viewer', shortcut: 'Ctrl+Alt+V', category: 'aps', tab: 'aps', panel: 'viewer', commandType: 'button', implementationTarget: 'TASK 010', action: 'aps.viewer', enabled: true, visible: true, availability: ['always'], placeholder: true },
      { id: 'model-derivative', name: 'model-derivative', label: 'Model Derivative', shortcut: 'Ctrl+Alt+M', category: 'aps', tab: 'aps', panel: 'derivative', commandType: 'button', implementationTarget: 'TASK 010', action: 'aps.derivative', enabled: true, visible: true, availability: ['always'], placeholder: true },
      { id: 'data-management', name: 'data-management', label: 'Data Management', shortcut: 'Ctrl+Alt+D', category: 'aps', tab: 'aps', panel: 'data', commandType: 'button', implementationTarget: 'TASK 010', action: 'aps.data', enabled: true, visible: true, availability: ['always'], placeholder: true },
      { id: 'aps-automation', name: 'aps-automation', label: 'Automation', shortcut: 'Ctrl+Alt+A', category: 'aps', tab: 'aps', panel: 'automation', commandType: 'button', implementationTarget: 'TASK 011', action: 'aps.automation', enabled: true, visible: true, availability: ['always'], placeholder: true },
      { id: 'webhooks', name: 'webhooks', label: 'Webhooks', shortcut: 'Ctrl+Alt+W', category: 'aps', tab: 'aps', panel: 'webhooks', commandType: 'button', implementationTarget: 'TASK 010', action: 'aps.webhooks', enabled: true, visible: true, availability: ['always'], placeholder: true },
    ],
  },
  {
    id: 'datumbim',
    label: 'DATUMBIM',
    commands: [
      { id: 'sdk-manager', name: 'sdk-manager', label: 'SDK Manager', shortcut: 'Ctrl+Alt+S', category: 'datumbim', tab: 'datumbim', panel: 'core', commandType: 'button', implementationTarget: 'TASK 008', action: 'datumbim.sdk', enabled: true, visible: true, availability: ['always'] },
      { id: 'api-manager', name: 'api-manager', label: 'API Manager', shortcut: 'Ctrl+Alt+I', category: 'datumbim', tab: 'datumbim', panel: 'core', commandType: 'button', implementationTarget: 'TASK 006', action: 'datumbim.api', enabled: true, visible: true, availability: ['always'], placeholder: true },
      { id: 'addin-manager', name: 'addin-manager', label: 'Add-in Manager', shortcut: 'Ctrl+Alt+N', category: 'datumbim', tab: 'datumbim', panel: 'core', commandType: 'button', implementationTarget: 'TASK 008', action: 'datumbim.addins', enabled: true, visible: true, availability: ['always'], placeholder: true },
      { id: 'resource-browser', name: 'resource-browser', label: 'Resource Browser', shortcut: 'Ctrl+Alt+R', category: 'datumbim', tab: 'datumbim', panel: 'core', commandType: 'button', implementationTarget: 'TASK 009', action: 'datumbim.resources', enabled: true, visible: true, availability: ['always'] },
      { id: 'automation-console', name: 'automation-console', label: 'Automation Console', shortcut: 'Ctrl+Alt+C', category: 'datumbim', tab: 'datumbim', panel: 'core', commandType: 'button', implementationTarget: 'TASK 011', action: 'datumbim.automation', enabled: true, visible: true, availability: ['always'], placeholder: true },
    ],
  },
]

export const ALL_COMMANDS = COMMAND_CATEGORIES.flatMap((cat) => cat.commands)
