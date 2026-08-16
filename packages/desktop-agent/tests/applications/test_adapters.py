import pytest

from desktop_agent.applications.revit import RevitAdapter
from desktop_agent.applications.autocad import AutoCADAdapter
from desktop_agent.applications.navisworks import NavisworksAdapter
from desktop_agent.applications.dynamo import DynamoAdapter
from desktop_agent.applications.blender import BlenderAdapter
from desktop_agent.applications.browser import BrowserAdapter
from desktop_agent.applications.generic import GenericWindowsApplicationAdapter
from desktop_agent.applications.registry import ApplicationAdapterRegistry
from desktop_agent.models import ApplicationInfo, WindowInfo
from desktop_agent.session_manager import SessionManager
from desktop_agent.discovery import ApplicationDiscovery, WindowDiscovery


class TestDiscovery:
    def test_application_discovery_returns_list(self) -> None:
        discovery = ApplicationDiscovery()
        result = discovery.discover()
        assert isinstance(result, list)

    def test_window_discovery_returns_list(self) -> None:
        discovery = WindowDiscovery()
        result = discovery.discover_windows()
        assert isinstance(result, list)


class TestSessionBinding:
    def test_start_session_creates_session(self) -> None:
        manager = SessionManager()
        session = manager.start_session("unknown_app")
        assert session.application_id == "unknown_app"
        assert session.session_id is not None

    def test_attach_session_returns_none_for_missing_app(self) -> None:
        manager = SessionManager()
        session = manager.attach_session("unknown_app")
        assert session is None

    def test_get_session_returns_none_for_unknown(self) -> None:
        manager = SessionManager()
        assert manager.get_session("unknown-session") is None

    def test_close_session_returns_false_for_unknown(self) -> None:
        manager = SessionManager()
        assert manager.close_session("unknown-session") is False

    def test_detach_session_returns_false_for_unknown(self) -> None:
        manager = SessionManager()
        assert manager.detach_session("unknown-session") is False

    def test_restart_session_returns_none_for_unknown(self) -> None:
        manager = SessionManager()
        assert manager.restart_session("unknown-session") is None

    def test_get_sessions_returns_list(self) -> None:
        manager = SessionManager()
        assert isinstance(manager.get_sessions(), list)


class TestApplicationDetection:
    def test_revit_detection_not_running(self) -> None:
        app = ApplicationInfo(id="revit", name="Revit", display_name="Revit", running=False)
        adapter = RevitAdapter(app)
        result = adapter.is_available()
        assert result.status == "completed"
        assert "not_running" in result.result.lower() or "not_installed" in result.result.lower()

    def test_autocad_detection_not_running(self) -> None:
        app = ApplicationInfo(id="autocad", name="AutoCAD", display_name="AutoCAD", running=False)
        adapter = AutoCADAdapter(app)
        result = adapter.is_available()
        assert result.status == "completed"

    def test_navisworks_detection_not_running(self) -> None:
        app = ApplicationInfo(id="navisworks", name="Navisworks", display_name="Navisworks", running=False)
        adapter = NavisworksAdapter(app)
        result = adapter.is_available()
        assert result.status == "completed"

    def test_dynamo_detection_not_running(self) -> None:
        app = ApplicationInfo(id="dynamo", name="Dynamo", display_name="Dynamo", running=False)
        adapter = DynamoAdapter(app)
        result = adapter.is_available()
        assert result.status == "completed"

    def test_blender_detection_not_running(self) -> None:
        app = ApplicationInfo(id="blender", name="Blender", display_name="Blender", running=False)
        adapter = BlenderAdapter(app)
        result = adapter.is_available()
        assert result.status == "completed"

    def test_browser_detection_not_running(self) -> None:
        app = ApplicationInfo(id="browser", name="Browser", display_name="Browser", running=False)
        adapter = BrowserAdapter(app)
        result = adapter.is_available()
        assert result.status == "completed"

    def test_generic_adapter_without_application_fails(self) -> None:
        adapter = GenericWindowsApplicationAdapter()
        result = adapter.is_available()
        assert result.status == "failed"


class TestCapabilities:
    def test_revit_capabilities_when_not_running(self) -> None:
        app = ApplicationInfo(id="revit", name="Revit", display_name="Revit", running=False)
        adapter = RevitAdapter(app)
        capabilities = adapter.get_capabilities()
        assert capabilities.application_id == "revit"
        assert capabilities.ui_control_support is True
        assert "ui_control" in capabilities.capabilities

    def test_generic_adapter_capabilities(self) -> None:
        app = ApplicationInfo(id="generic", name="Generic", display_name="Generic", running=False)
        adapter = GenericWindowsApplicationAdapter(app)
        capabilities = adapter.get_capabilities()
        assert capabilities.automation_support is True
        assert capabilities.ui_control_support is True
