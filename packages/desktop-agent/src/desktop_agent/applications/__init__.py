from __future__ import annotations

from desktop_agent.applications.base import ApplicationAdapter
from desktop_agent.applications.registry import ApplicationAdapterRegistry
from desktop_agent.applications.generic import GenericWindowsApplicationAdapter
from desktop_agent.applications.revit import RevitAdapter
from desktop_agent.applications.autocad import AutoCADAdapter
from desktop_agent.applications.navisworks import NavisworksAdapter
from desktop_agent.applications.dynamo import DynamoAdapter
from desktop_agent.applications.pyrevit import PyRevitAdapter
from desktop_agent.applications.blender import BlenderAdapter
from desktop_agent.applications.browser import BrowserAdapter


def create_default_registry() -> ApplicationAdapterRegistry:
    registry = ApplicationAdapterRegistry()
    registry.register("revit", RevitAdapter)
    registry.register("autocad", AutoCADAdapter)
    registry.register("navisworks", NavisworksAdapter)
    registry.register("dynamo", DynamoAdapter)
    registry.register("pyrevit", PyRevitAdapter)
    registry.register("blender", BlenderAdapter)
    registry.register("browser", BrowserAdapter)
    registry.register_fallback(GenericWindowsApplicationAdapter)
    return registry
