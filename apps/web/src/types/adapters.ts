export interface ApiClientConfig {
  baseUrl: string
  timeout: number
  retries: number
}

export interface ApiResponse<T> {
  data: T | null
  error: string | null
  status: number
}

export interface ServiceLayerAdapter {
  name: string
  available: boolean
  version?: string
  endpoint?: string
}

export interface APSClientConfig {
  clientId: string
  clientSecret: string
  redirectUri: string
  scopes: string[]
  environment: 'production' | 'staging' | 'local'
}

export interface APSViewerConfig {
  documentId: string
  urn: string
  env?: string
}

export const DEFAULT_API_CONFIG: ApiClientConfig = {
  baseUrl: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  timeout: 30000,
  retries: 3,
}

export const APS_ADAPTER: ServiceLayerAdapter = {
  name: 'Autodesk Platform Services',
  available: false,
  version: undefined,
  endpoint: 'https://developer.api.autodesk.com',
}

export const REVIT_ADAPTER: ServiceLayerAdapter = {
  name: 'Revit Engine',
  available: false,
  version: undefined,
}

export const AUTOCAD_ADAPTER: ServiceLayerAdapter = {
  name: 'AutoCAD Engine',
  available: false,
  version: undefined,
}

export const NAVISWORKS_ADAPTER: ServiceLayerAdapter = {
  name: 'Navisworks Engine',
  available: false,
  version: undefined,
}

export const IFC_ADAPTER: ServiceLayerAdapter = {
  name: 'IFC Engine',
  available: false,
  version: undefined,
}

export const ENGINE_ADAPTERS: ServiceLayerAdapter[] = [
  REVIT_ADAPTER,
  AUTOCAD_ADAPTER,
  NAVISWORKS_ADAPTER,
  IFC_ADAPTER,
]
