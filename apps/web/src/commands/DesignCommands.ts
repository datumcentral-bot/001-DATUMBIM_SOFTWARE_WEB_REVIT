import { useDesignSlice } from '@/store/slices/designSlice'
import type { DesignSliceState } from '@/store/slices/designSlice'

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

  static navigateToLevel = async (_ctx: DesignCommandContext, _levelId: string) => {
    return { success: true, message: 'Navigation to level — placeholder' }
  }

  static navigateToView = async (_ctx: DesignCommandContext, _viewId: string) => {
    return { success: true, message: 'Navigation to view — placeholder' }
  }
}
