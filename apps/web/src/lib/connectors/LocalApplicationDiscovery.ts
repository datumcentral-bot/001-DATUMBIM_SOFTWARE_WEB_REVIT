export interface LocalApplication {
  id: string
  name: string
  displayName: string
  version?: string
  installPath?: string
  executable?: string
  running: boolean
  processId?: number
  capabilities: string[]
}

export class LocalApplicationDiscovery {
  private applications: LocalApplication[] = []

  constructor() {
    this.applications = [
      {
        id: 'revit',
        name: 'Revit',
        displayName: 'Autodesk Revit',
        version: undefined,
        installPath: undefined,
        executable: 'Revit.exe',
        running: false,
        capabilities: ['api', 'pyrevit', 'dynamo', 'screen', 'file'],
      },
      {
        id: 'autocad',
        name: 'AutoCAD',
        displayName: 'Autodesk AutoCAD',
        version: undefined,
        installPath: undefined,
        executable: 'acad.exe',
        running: false,
        capabilities: ['api', 'plugin', 'script', 'screen', 'file'],
      },
      {
        id: 'navisworks',
        name: 'Navisworks',
        displayName: 'Autodesk Navisworks',
        version: undefined,
        installPath: undefined,
        executable: 'Navisworks.exe',
        running: false,
        capabilities: ['api', 'plugin', 'script', 'screen', 'file'],
      },
      {
        id: 'dynamo',
        name: 'Dynamo',
        displayName: 'Dynamo',
        version: undefined,
        installPath: undefined,
        executable: 'Dynamo.exe',
        running: false,
        capabilities: ['script', 'automation', 'file'],
      },
      {
        id: 'blender',
        name: 'Blender',
        displayName: 'Blender',
        version: undefined,
        installPath: undefined,
        executable: 'blender.exe',
        running: false,
        capabilities: ['api', 'script', 'screen', 'file'],
      },
    ]
  }

  discover(): LocalApplication[] {
    return this.applications.map((app) => ({
      ...app,
      running: this.checkIfRunning(app.executable),
    }))
  }

  getById(id: string): LocalApplication | undefined {
    return this.applications.find((app) => app.id === id)
  }

  getRunning(): LocalApplication[] {
    return this.applications.filter((app) => app.running)
  }

  private checkIfRunning(executable?: string): boolean {
    if (!executable) return false
    return false
  }
}
