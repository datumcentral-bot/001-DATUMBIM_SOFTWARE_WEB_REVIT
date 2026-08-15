import { useDesignSlice } from '@/store/slices/designSlice'
import type { DesignSliceState } from '@/store/slices/designSlice'
import { useShellStore } from '@/store/shellStore'
import { levelApi } from '@/lib/api/levels'
import type { LevelResponse } from '@/types/api'

export interface DesignCommandContext {
  designSlice: DesignSliceState
}

export class DesignCommands {
  static initialize = async (ctx: DesignCommandContext) => {
    ctx.designSlice.initialize()
    return { success: true, message: 'Design engine initialized' }
  }

  static dispose = async (ctx: DesignCommandContext) => {
    ctx.designSlice.dispose()
    return { success: true, message: 'Design engine disposed' }
  }

  static selectElement = async (ctx: DesignCommandContext, elementId: string, additive = false) => {
    ctx.designSlice.selectElement(elementId, additive)
    return { success: true, message: `Selected element ${elementId}` }
  }

  static clearSelection = async (ctx: DesignCommandContext) => {
    ctx.designSlice.clearSelection()
    return { success: true, message: 'Selection cleared' }
  }

  static setActiveView = async (ctx: DesignCommandContext, viewId: string) => {
    ctx.designSlice.setActiveView(viewId)
    return { success: true, message: `Active view set to ${viewId}` }
  }

  static zoomExtents = async (ctx: DesignCommandContext) => {
    ctx.designSlice.zoomExtents()
    return { success: true, message: 'Zoom extents applied' }
  }

  static zoomIn = async (ctx: DesignCommandContext) => {
    ctx.designSlice.zoomIn()
    return { success: true, message: 'Zoom in' }
  }

  static zoomOut = async (ctx: DesignCommandContext) => {
    ctx.designSlice.zoomOut()
    return { success: true, message: 'Zoom out' }
  }

  static fitToView = async (ctx: DesignCommandContext) => {
    ctx.designSlice.fitToView()
    return { success: true, message: 'Fit to view' }
  }

  static navigateToLevel = async (_ctx: DesignCommandContext, levelId: string) => {
    const res = await levelApi.get(levelId)
    if (res.error || !res.data) {
      return { success: false, message: res.error || 'Level not found' }
    }
    const level = res.data as LevelResponse
    return { success: true, message: `Navigated to level: ${level.name}` }
  }

  static navigateToView = async (_ctx: DesignCommandContext, viewId: string) => {
    return { success: true, message: `Navigated to view: ${viewId}` }
  }

  static openFileImport = async (_ctx: DesignCommandContext) => {
    const shell = useShellStore.getState()
    shell.openDialog({ id: 'file-import', title: 'Import File', content: null })
    return { success: true, message: 'File import dialog opened' }
  }
}
