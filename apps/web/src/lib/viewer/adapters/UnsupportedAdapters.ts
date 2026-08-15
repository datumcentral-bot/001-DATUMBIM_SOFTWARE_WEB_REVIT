import type { ModelLoader } from './FormatAdapters'

export class UnsupportedAdapter implements ModelLoader {
  constructor(private readonly formatName: string) {}

  loadModel(_data: unknown): never {
    throw new Error(`${this.formatName} format is not yet supported`)
  }
}

export const RVTAdapter = new UnsupportedAdapter('RVT')
export const IFCAdapter = new UnsupportedAdapter('IFC')
export const DWGAdapter = new UnsupportedAdapter('DWG')
export const DXFAdapter = new UnsupportedAdapter('DXF')
export const NWDAdapter = new UnsupportedAdapter('NWD')
export const NWCAdapter = new UnsupportedAdapter('NWC')
export const OBJAdapter = new UnsupportedAdapter('OBJ')
export const FBXAdapter = new UnsupportedAdapter('FBX')
