/// <reference types="vitest/globals" />

import { describe, it, expect, beforeEach } from 'vitest'
import { InMemoryConnectorRegistry } from '@/lib/connectors/ConnectorRegistry'
import type { ApplicationConnector, ApplicationCapability, ApplicationSession } from '@/lib/connectors/types/ConnectorTypes'

const createMockConnector = (id: string, name: string): ApplicationConnector => ({
  id,
  name,
  description: `Mock connector ${name}`,
  status: 'discovered',
  capabilities: [
    {
      id: `${id}-api`,
      name: 'API',
      description: 'API capability',
      channel: 'api',
      riskLevel: 'medium',
      available: true,
    },
  ],
  sessions: [],
  discover: async () => [],
  connect: async () => ({ id: `${id}-session-1`, applicationId: id, status: 'connected', capabilities: [] }),
  disconnect: async () => {},
  execute: async () => ({ id: `${id}-job-1`, commandId: 'test', status: 'pending' }),
  getStatus: async () => 'discovered',
})

describe('InMemoryConnectorRegistry', () => {
  let registry: InMemoryConnectorRegistry

  beforeEach(() => {
    registry = new InMemoryConnectorRegistry()
  })

  it('registers and retrieves a connector', () => {
    const connector = createMockConnector('revit', 'Revit')
    registry.register(connector)
    expect(registry.get('revit')).toBe(connector)
  })

  it('returns undefined for missing connector', () => {
    expect(registry.get('missing')).toBeUndefined()
  })

  it('lists all connectors', () => {
    registry.register(createMockConnector('revit', 'Revit'))
    registry.register(createMockConnector('autocad', 'AutoCAD'))
    const all = registry.getAll()
    expect(all).toHaveLength(2)
    expect(all.map((c) => c.id).sort()).toEqual(['autocad', 'revit'])
  })

  it('unregisters a connector', () => {
    registry.register(createMockConnector('revit', 'Revit'))
    registry.unregister('revit')
    expect(registry.get('revit')).toBeUndefined()
    expect(registry.getAll()).toHaveLength(0)
  })

  it('filters connectors by status', () => {
    const connected = createMockConnector('revit', 'Revit')
    connected.status = 'connected'
    registry.register(connected)
    registry.register(createMockConnector('autocad', 'AutoCAD'))
    const connectedOnly = registry.getByStatus('connected')
    expect(connectedOnly).toHaveLength(1)
    expect(connectedOnly[0].id).toBe('revit')
  })
})

describe('Connector types', () => {
  it('allows constructing a valid ApplicationCapability', () => {
    const capability: ApplicationCapability = {
      id: 'test-cap',
      name: 'Test',
      channel: 'api',
      riskLevel: 'low',
      available: true,
    }
    expect(capability.id).toBe('test-cap')
    expect(capability.available).toBe(true)
  })

  it('allows constructing a valid ApplicationSession', () => {
    const session: ApplicationSession = {
      id: 'session-1',
      applicationId: 'revit',
      status: 'connected',
      capabilities: [],
    }
    expect(session.status).toBe('connected')
  })
})
