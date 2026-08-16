import pytest

from desktop_agent.applications.registry import ApplicationAdapterRegistry
from desktop_agent.applications.generic import GenericWindowsApplicationAdapter
from desktop_agent.applications.revit import RevitAdapter
from desktop_agent.applications.autocad import AutoCADAdapter
from desktop_agent.applications.navisworks import NavisworksAdapter
from desktop_agent.applications.dynamo import DynamoAdapter
from desktop_agent.applications.pyrevit import PyRevitAdapter
from desktop_agent.applications.blender import BlenderAdapter
from desktop_agent.applications.browser import BrowserAdapter
from desktop_agent.models import ApplicationInfo


class TestRegistry:
    def test_register_and_get(self) -> None:
        registry = ApplicationAdapterRegistry()
        registry.register("revit", RevitAdapter)
        assert registry.get("revit") is RevitAdapter

    def test_unregister(self) -> None:
        registry = ApplicationAdapterRegistry()
        registry.register("revit", RevitAdapter)
        registry.unregister("revit")
        assert registry.get("revit") is None

    def test_list_returns_registered(self) -> None:
        registry = ApplicationAdapterRegistry()
        registry.register("revit", RevitAdapter)
        registry.register("autocad", AutoCADAdapter)
        assert "revit" in registry.list()
        assert "autocad" in registry.list()

    def test_resolve_known_application(self) -> None:
        registry = ApplicationAdapterRegistry()
        registry.register("revit", RevitAdapter)
        adapter = registry.resolve("revit")
        assert isinstance(adapter, RevitAdapter)

    def test_resolve_unknown_uses_fallback(self) -> None:
        registry = ApplicationAdapterRegistry()
        registry.register_fallback(GenericWindowsApplicationAdapter)
        adapter = registry.resolve("unknown_app")
        assert isinstance(adapter, GenericWindowsApplicationAdapter)

    def test_resolve_unknown_without_fallback_raises(self) -> None:
        registry = ApplicationAdapterRegistry()
        with pytest.raises(ValueError):
            registry.resolve("unknown_app")

    def test_detect_from_application_info(self) -> None:
        registry = ApplicationAdapterRegistry()
        registry.register("revit", RevitAdapter)
        application = ApplicationInfo(id="revit", name="Revit", display_name="Revit", running=True)
        adapter = registry.detect(application)
        assert isinstance(adapter, RevitAdapter)

    def test_duplicate_register_overwrites(self) -> None:
        registry = ApplicationAdapterRegistry()
        registry.register("revit", RevitAdapter)
        registry.register("revit", RevitAdapter)
        assert registry.get("revit") is RevitAdapter


class TestAdapters:
    def test_revit_adapter_identify(self) -> None:
        adapter = RevitAdapter()
        result = adapter.identify()
        assert result.status == "completed"

    def test_autocad_adapter_identify(self) -> None:
        adapter = AutoCADAdapter()
        result = adapter.identify()
        assert result.status == "completed"

    def test_navisworks_adapter_identify(self) -> None:
        adapter = NavisworksAdapter()
        result = adapter.identify()
        assert result.status == "completed"

    def test_dynamo_adapter_identify(self) -> None:
        adapter = DynamoAdapter()
        result = adapter.identify()
        assert result.status == "completed"

    def test_pyrevit_adapter_identify(self) -> None:
        adapter = PyRevitAdapter()
        result = adapter.identify()
        assert result.status == "completed"

    def test_blender_adapter_identify(self) -> None:
        adapter = BlenderAdapter()
        result = adapter.identify()
        assert result.status == "completed"

    def test_browser_adapter_identify(self) -> None:
        adapter = BrowserAdapter()
        result = adapter.identify()
        assert result.status == "completed"

    def test_generic_adapter_rejects_unsupported_action(self) -> None:
        from desktop_agent.control.models import ActionRequest, ActionResult
        from datetime import UTC, datetime

        adapter = GenericWindowsApplicationAdapter()
        request = ActionRequest(
            action_id="1",
            session_id="s1",
            application_id="generic",
            action_type="unsupported_action",
            timestamp=datetime.now(tz=UTC),
        )
        result = adapter.execute(request)
        assert result.status == "failed"
        assert "Unsupported action for generic adapter" in (result.error or "")
