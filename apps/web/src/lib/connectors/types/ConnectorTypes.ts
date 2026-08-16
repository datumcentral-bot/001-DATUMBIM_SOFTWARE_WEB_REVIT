export type ApplicationStatus = 'unknown' | 'discovered' | 'configured' | 'connected' | 'authenticated' | 'available' | 'executable' | 'verified' | 'error'

export type ExecutionChannel = 'api' | 'sdk' | 'plugin' | 'script' | 'automation' | 'screen' | 'file'

export type RiskLevel = 'low' | 'medium' | 'high'

export interface ApplicationCapability {
  id: string
  name: string
  description?: string
  channel: ExecutionChannel
  riskLevel: RiskLevel
  available: boolean
  metadata?: Record<string, unknown>
}

export interface ApplicationCommand {
  id: string
  name: string
  description?: string
  capabilityId: string
  parameters?: Record<string, unknown>
  riskLevel: RiskLevel
  approvalRequired: boolean
}

export interface ApplicationJob {
  id: string
  commandId: string
  status: 'pending' | 'running' | 'completed' | 'failed' | 'cancelled'
  progress?: number
  result?: unknown
  error?: string
  logs?: string[]
  startedAt?: string
  finishedAt?: string
}

export interface ApplicationSession {
  id: string
  applicationId: string
  status: ApplicationStatus
  capabilities: ApplicationCapability[]
  activeJobId?: string
  metadata?: Record<string, unknown>
}

export interface ApplicationConnector {
  id: string
  name: string
  description?: string
  status: ApplicationStatus
  version?: string
  capabilities: ApplicationCapability[]
  sessions: ApplicationSession[]
  discover(): Promise<ApplicationCapability[]>
  connect(): Promise<ApplicationSession>
  disconnect(sessionId: string): Promise<void>
  execute(sessionId: string, commandId: string, parameters?: Record<string, unknown>): Promise<ApplicationJob>
  getStatus(): Promise<ApplicationStatus>
}

export interface ConnectorRegistry {
  register(connector: ApplicationConnector): void
  unregister(connectorId: string): void
  get(connectorId: string): ApplicationConnector | undefined
  getAll(): ApplicationConnector[]
  getByStatus(status: ApplicationStatus): ApplicationConnector[]
}

export interface SessionRegistry {
  register(session: ApplicationSession): void
  unregister(sessionId: string): void
  get(sessionId: string): ApplicationSession | undefined
  getByApplication(applicationId: string): ApplicationSession[]
  getAll(): ApplicationSession[]
}

export interface CommandRegistry {
  register(command: ApplicationCommand): void
  unregister(commandId: string): void
  get(commandId: string): ApplicationCommand | undefined
  getByCapability(capabilityId: string): ApplicationCommand[]
  getAll(): ApplicationCommand[]
}

export interface JobRegistry {
  register(job: ApplicationJob): void
  unregister(jobId: string): void
  get(jobId: string): ApplicationJob | undefined
  getBySession(sessionId: string): ApplicationJob[]
  getAll(): ApplicationJob[]
}
