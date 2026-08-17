export const RIBBON_TABS = [
  { id: 'home', label: 'Home' },
  { id: 'applications', label: 'Applications' },
  { id: 'sessions', label: 'Sessions' },
  { id: 'observation', label: 'Observation' },
  { id: 'live-application', label: 'Live Application' },
  { id: 'control', label: 'Control' },
  { id: 'ai', label: 'AI' },
  { id: 'planner', label: 'Planner' },
  { id: 'revit', label: 'Revit' },
  { id: 'integrations', label: 'Integrations' },
  { id: 'agents', label: 'Agents' },
  { id: 'workflows', label: 'Workflows' },
  { id: 'settings', label: 'Settings' },
] as const

export const RIBBON_PANELS: Record<string, { id: string; label: string; items: { id: string; label: string; icon?: string }[] }[]> = {
  home: [
    {
      id: 'dashboard',
      label: 'Dashboard',
      items: [
        { id: 'system-health', label: 'System Health', icon: '📊' },
        { id: 'recent-sessions', label: 'Recent Sessions', icon: '🕒' },
        { id: 'recent-applications', label: 'Recent Applications', icon: '💻' },
      ],
    },
  ],
  applications: [
    {
      id: 'connect',
      label: 'Connect',
      items: [
        { id: 'revit', label: 'Revit', icon: '🏗️' },
        { id: 'autocad', label: 'AutoCAD', icon: '📐' },
        { id: 'navisworks', label: 'Navisworks', icon: '🔍' },
        { id: 'dynamo', label: 'Dynamo', icon: '⚡' },
        { id: 'blender', label: 'Blender', icon: '🟢' },
      ],
    },
    {
      id: 'discovery',
      label: 'Discovery',
      items: [
        { id: 'discover-apps', label: 'Discover Apps', icon: '🔎' },
        { id: 'discover-connectors', label: 'Connectors', icon: '🔌' },
      ],
    },
  ],
  sessions: [
    {
      id: 'lifecycle',
      label: 'Lifecycle',
      items: [
        { id: 'start-session', label: 'Start Session', icon: '▶️' },
        { id: 'attach-session', label: 'Attach', icon: '🔗' },
        { id: 'detach-session', label: 'Detach', icon: '🚪' },
        { id: 'restart-session', label: 'Restart', icon: '🔄' },
        { id: 'close-session', label: 'Close', icon: '⏹️' },
      ],
    },
  ],
  observation: [
    {
      id: 'capture',
      label: 'Capture',
      items: [
        { id: 'capture-screen', label: 'Capture Screen', icon: '📸' },
        { id: 'capture-window', label: 'Capture Window', icon: '🪟' },
        { id: 'observe-window', label: 'Observe Window', icon: '👁️' },
      ],
    },
  ],
  control: [
    {
      id: 'input',
      label: 'Input',
      items: [
        { id: 'mouse-move', label: 'Mouse Move', icon: '🖱️' },
        { id: 'mouse-click', label: 'Mouse Click', icon: '👆' },
        { id: 'keyboard-type', label: 'Keyboard Type', icon: '⌨️' },
        { id: 'hotkey', label: 'Hotkey', icon: '🔑' },
      ],
    },
    {
      id: 'window',
      label: 'Window',
      items: [
        { id: 'activate-window', label: 'Activate', icon: '🪟' },
        { id: 'minimize-window', label: 'Minimize', icon: '➖' },
        { id: 'maximize-window', label: 'Maximize', icon: '🔲' },
        { id: 'close-window', label: 'Close', icon: '❌' },
      ],
    },
    {
      id: 'application',
      label: 'Application',
      items: [
        { id: 'launch-application', label: 'Launch', icon: '🚀' },
        { id: 'focus-application', label: 'Focus', icon: '🎯' },
        { id: 'close-application', label: 'Close', icon: '⏹️' },
      ],
    },
  ],
  agents: [
    {
      id: 'ai-agents',
      label: 'AI Agents',
      items: [
        { id: 'bim-agent', label: 'BIM Agent', icon: '🤖' },
        { id: 'revit-agent', label: 'Revit Agent', icon: '🏗️' },
        { id: 'mep-agent', label: 'MEP Agent', icon: '🔧' },
        { id: 'qa-agent', label: 'QA Agent', icon: '✅' },
      ],
    },
  ],
  workflows: [
    {
      id: 'automation',
      label: 'Automation',
      items: [
        { id: 'n8n-workflows', label: 'n8n Workflows', icon: '🔄' },
        { id: 'dynamo-graphs', label: 'Dynamo Graphs', icon: '⚡' },
        { id: 'pyrevit-scripts', label: 'pyRevit Scripts', icon: '🐍' },
      ],
    },
  ],
  ai: [
    {
      id: 'providers',
      label: 'Providers',
      items: [
        { id: 'ai-providers', label: 'Providers', icon: '🧠' },
        { id: 'ai-models', label: 'Models', icon: '📦' },
        { id: 'ai-health', label: 'Health', icon: '💓' },
      ],
    },
    {
      id: 'vision',
      label: 'Vision',
      items: [
        { id: 'analyze-observation', label: 'Analyze Observation', icon: '👁️' },
        { id: 'detect-ui', label: 'Detect UI', icon: '🖥️' },
        { id: 'detect-text', label: 'Detect Text', icon: '📝' },
      ],
    },
  ],
  planner: [
    {
      id: 'planning',
      label: 'Planning',
      items: [
        { id: 'create-plan', label: 'Create Plan', icon: '📝' },
        { id: 'validate-plan', label: 'Validate Plan', icon: '✅' },
        { id: 'explain-plan', label: 'Explain Plan', icon: '📖' },
      ],
    },
  ],
  revit: [
    {
      id: 'intelligence',
      label: 'Intelligence',
      items: [
        { id: 'revit-status', label: 'Status', icon: '📡' },
        { id: 'revit-categories', label: 'Categories', icon: '📂' },
        { id: 'revit-elements', label: 'Elements', icon: '🧱' },
        { id: 'revit-families', label: 'Families', icon: '📦' },
        { id: 'revit-views', label: 'Views', icon: '👁️' },
      ],
    },
    {
      id: 'operations',
      label: 'Operations',
      items: [
        { id: 'revit-connect', label: 'Connect', icon: '🔌' },
        { id: 'revit-discover', label: 'Discover', icon: '🔍' },
        { id: 'revit-query', label: 'Query', icon: '💬' },
      ],
    },
  ],
  settings: [
    {
      id: 'config',
      label: 'Configuration',
      items: [
        { id: 'project-settings', label: 'Project Settings', icon: '📁' },
        { id: 'agent-settings', label: 'Agent Settings', icon: '🤖' },
        { id: 'connector-settings', label: 'Connector Settings', icon: '🔌' },
      ],
    },
  ],
}

export const DEFAULT_VIEW_TABS: { id: string; label: string; type: '3d' | 'floor-plan' | 'ceiling-plan' | 'elevation' | 'section' | 'detail' | 'schedule' | 'sheet' | 'drafting' | 'browser' | 'model' | 'applications' | 'sessions' | 'observation' | 'control' | 'ai' | 'planner' | 'revit' | 'live-application' | 'integrations' | 'execution' | 'workflows' }[] = [
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
  { id: 'control', label: 'Control', type: 'control' },
  { id: 'ai', label: 'AI', type: 'ai' },
  { id: 'planner', label: 'Planner', type: 'planner' },
  { id: 'revit', label: 'Revit', type: 'revit' },
  { id: 'live-application', label: 'Live Application', type: 'live-application' },
  { id: 'integrations', label: 'Integrations', type: 'integrations' },
  { id: 'execution', label: 'Execution', type: 'execution' },
  { id: 'workflows', label: 'Workflows', type: 'workflows' },
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
