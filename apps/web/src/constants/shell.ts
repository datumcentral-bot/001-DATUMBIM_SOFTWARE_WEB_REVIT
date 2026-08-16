export const RIBBON_TABS = [
  { id: 'architecture', label: 'Architecture' },
  { id: 'structure', label: 'Structure' },
  { id: 'mep', label: 'MEP' },
  { id: 'insert', label: 'Insert' },
  { id: 'annotate', label: 'Annotate' },
  { id: 'view', label: 'View' },
  { id: 'manage', label: 'Manage' },
  { id: 'collaborate', label: 'Collaborate' },
  { id: 'analyze', label: 'Analyze' },
  { id: 'automate', label: 'Automate' },
  { id: 'datumbim', label: 'DATUMBIM' },
] as const

export const RIBBON_PANELS: Record<string, { id: string; label: string; items: { id: string; label: string; icon?: string }[] }[]> = {
  architecture: [
    {
      id: 'build',
      label: 'Build',
      items: [
        { id: 'wall', label: 'Wall', icon: '📐' },
        { id: 'door', label: 'Door', icon: '🚪' },
        { id: 'window', label: 'Window', icon: '🪟' },
        { id: 'roof', label: 'Roof', icon: '🏠' },
        { id: 'floor', label: 'Floor', icon: '⬜' },
      ],
    },
    {
      id: 'model',
      label: 'Model',
      items: [
        { id: 'column', label: 'Column', icon: '🏛️' },
        { id: 'beam', label: 'Beam', icon: '🔲' },
        { id: 'grid', label: 'Grid', icon: '➕' },
        { id: 'level', label: 'Level', icon: '📏' },
      ],
    },
  ],
  structure: [
    {
      id: 'structural',
      label: 'Structural',
      items: [
        { id: 'struct-column', label: 'Column', icon: '🏛️' },
        { id: 'struct-beam', label: 'Beam', icon: '🔲' },
        { id: 'struct-floor', label: 'Floor', icon: '⬜' },
        { id: 'struct-foundation', label: 'Foundation', icon: '🧱' },
      ],
    },
  ],
  mep: [
    {
      id: 'systems',
      label: 'Systems',
      items: [
        { id: 'duct', label: 'Duct', icon: '🔼' },
        { id: 'pipe', label: 'Pipe', icon: '🔧' },
        { id: 'cable-tray', label: 'Cable Tray', icon: '🔌' },
        { id: 'conduit', label: 'Conduit', icon: '⚡' },
      ],
    },
  ],
  insert: [
    {
      id: 'load',
      label: 'Load',
      items: [
        { id: 'load-family', label: 'Load Family', icon: '📦' },
        { id: 'link-revit', label: 'Link Revit', icon: '🔗' },
        { id: 'import-cad', label: 'Import CAD', icon: '📥' },
      ],
    },
  ],
  annotate: [
    {
      id: 'dimension',
      label: 'Dimension',
      items: [
        { id: 'linear-dim', label: 'Linear', icon: '📏' },
        { id: 'angular-dim', label: 'Angular', icon: '📐' },
        { id: 'radial-dim', label: 'Radial', icon: '⭕' },
      ],
    },
  ],
  view: [
    {
      id: 'create',
      label: 'Create',
      items: [
        { id: 'plan-view', label: 'Plan View', icon: '📋' },
        { id: 'section', label: 'Section', icon: '✂️' },
        { id: 'elevation', label: 'Elevation', icon: '📊' },
        { id: '3d-view', label: '3D View', icon: '🎲' },
      ],
    },
  ],
  manage: [
    {
      id: 'settings',
      label: 'Settings',
      items: [
        { id: 'project-info', label: 'Project Info', icon: 'ℹ️' },
        { id: 'materials', label: 'Materials', icon: '🎨' },
        { id: 'settings', label: 'Settings', icon: '⚙️' },
      ],
    },
  ],
  collaborate: [
    {
      id: 'worksharing',
      label: 'Worksharing',
      items: [
        { id: 'sync', label: 'Sync', icon: '🔄' },
        { id: 'reload', label: 'Reload', icon: '🔁' },
      ],
    },
  ],
  analyze: [
    {
      id: 'analysis',
      label: 'Analysis',
      items: [
        { id: 'clash', label: 'Clash Detection', icon: '💥' },
        { id: 'quantities', label: 'Quantities', icon: '📊' },
      ],
    },
  ],
  automate: [
    {
      id: 'automation',
      label: 'Automation',
      items: [
        { id: 'dynamo', label: 'Dynamo', icon: '⚡' },
        { id: 'python', label: 'Python', icon: '🐍' },
        { id: 'batch', label: 'Batch Process', icon: '📦' },
      ],
    },
  ],
  datumbim: [
    {
      id: 'core',
      label: 'DATUMBIM',
      items: [
        { id: 'resource-manager', label: 'Resource Manager', icon: '📚' },
        { id: 'sdk-manager', label: 'SDK Manager', icon: '🔧' },
        { id: 'format-manager', label: 'Format Manager', icon: '📄' },
        { id: 'settings', label: 'Settings', icon: '⚙️' },
      ],
    },
  ],
}

export const DEFAULT_VIEW_TABS: { id: string; label: string; type: '3d' | 'floor-plan' | 'ceiling-plan' | 'elevation' | 'section' | 'detail' | 'schedule' | 'sheet' | 'drafting' | 'browser' | 'model' | 'applications' | 'sessions' | 'observation' }[] = [
  { id: 'view-3d', label: '{3D}', type: '3d' },
  { id: 'floor-plan', label: 'Floor Plan', type: 'floor-plan' },
  { id: 'ceiling-plan', label: 'Ceiling Plan', type: 'ceiling-plan' },
  { id: 'elevation-1', label: 'Elevation 1', type: 'elevation' },
  { id: 'section-1', label: 'Section 1', type: 'section' },
  { id: 'detail-1', label: 'Detail 1', type: 'detail' },
  { id: 'schedule-1', label: 'Schedule 1', type: 'schedule' },
  { id: 'sheet-1', label: 'Sheet 1', type: 'sheet' },
  { id: 'drafting-1', label: 'Drafting 1', type: 'drafting' },
  { id: 'applications', label: 'Applications', type: 'applications' },
  { id: 'sessions', label: 'Sessions', type: 'sessions' },
  { id: 'observation', label: 'Observation', type: 'observation' },
]

export const COMMANDS = [
  { id: 'new-project', label: 'New Project', shortcut: 'Ctrl+N' },
  { id: 'open', label: 'Open', shortcut: 'Ctrl+O' },
  { id: 'save', label: 'Save', shortcut: 'Ctrl+S' },
  { id: 'undo', label: 'Undo', shortcut: 'Ctrl+Z' },
  { id: 'redo', label: 'Redo', shortcut: 'Ctrl+Y' },
  { id: 'cut', label: 'Cut', shortcut: 'Ctrl+X' },
  { id: 'copy', label: 'Copy', shortcut: 'Ctrl+C' },
  { id: 'paste', label: 'Paste', shortcut: 'Ctrl+V' },
  { id: 'delete', label: 'Delete', shortcut: 'Del' },
  { id: 'select-all', label: 'Select All', shortcut: 'Ctrl+A' },
  { id: 'zoom-extents', label: 'Zoom Extents', shortcut: 'Ctrl+E' },
  { id: 'zoom-in', label: 'Zoom In', shortcut: 'Ctrl+=', },
  { id: 'zoom-out', label: 'Zoom Out', shortcut: 'Ctrl+-' },
]
