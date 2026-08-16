import type { ApplicationConnector, ConnectorRegistry, ApplicationStatus } from './types/ConnectorTypes'

export class InMemoryConnectorRegistry implements ConnectorRegistry {
  private connectors: Map<string, ApplicationConnector> = new Map()

  register(connector: ApplicationConnector): void {
    this.connectors.set(connector.id, connector)
  }

  unregister(connectorId: string): void {
    this.connectors.delete(connectorId)
  }

  get(connectorId: string): ApplicationConnector | undefined {
    return this.connectors.get(connectorId)
  }

  getAll(): ApplicationConnector[] {
    return Array.from(this.connectors.values())
  }

  getByStatus(status: ApplicationStatus): ApplicationConnector[] {
    return this.getAll().filter((connector) => connector.status === status)
  }
}

export function createEmptyRegistry(): ConnectorRegistry {
  return new InMemoryConnectorRegistry()
}
