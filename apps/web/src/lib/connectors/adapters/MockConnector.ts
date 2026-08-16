import type { ApplicationConnector, ApplicationCapability, ApplicationSession, ApplicationJob } from '../types/ConnectorTypes'

export class MockApplicationConnector implements ApplicationConnector {
  id: string
  name: string
  description?: string
  status: 'discovered' | 'connected' = 'discovered'
  version?: string
  capabilities: ApplicationCapability[] = []
  sessions: ApplicationSession[] = []

  constructor(id: string, name: string, description?: string) {
    this.id = id
    this.name = name
    this.description = description
  }

  async discover(): Promise<ApplicationCapability[]> {
    this.status = 'discovered'
    return this.capabilities
  }

  async connect(): Promise<ApplicationSession> {
    this.status = 'connected'
    const session: ApplicationSession = {
      id: `${this.id}-session-${Date.now()}`,
      applicationId: this.id,
      status: 'connected',
      capabilities: this.capabilities,
    }
    this.sessions.push(session)
    return session
  }

  async disconnect(sessionId: string): Promise<void> {
    this.sessions = this.sessions.filter((s) => s.id !== sessionId)
    if (this.sessions.length === 0) {
      this.status = 'discovered'
    }
  }

  async execute(sessionId: string, commandId: string, parameters?: Record<string, unknown>): Promise<ApplicationJob> {
    const job: ApplicationJob = {
      id: `${this.id}-job-${Date.now()}`,
      commandId,
      status: 'pending',
      progress: 0,
      logs: [`Executing ${commandId} with parameters: ${JSON.stringify(parameters ?? {})}`],
    }
    return job
  }

  async getStatus(): Promise<'discovered' | 'connected'> {
    return this.status
  }
}
