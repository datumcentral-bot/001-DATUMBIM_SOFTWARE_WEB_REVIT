import pytest

from revit_model.discovery import RevitDiscovery
from revit_model.models import RevitCapability, RevitCategory, RevitCategoryGroup, RevitDocument, RevitElement, RevitFamily, RevitFamilyType, RevitLevel, RevitModelInfo, RevitParameter, RevitParameterStorageType, RevitParameterType, RevitView, RevitViewType
from revit_model.registry import RevitCapabilityRegistry


class TestRevitModels:
    def test_revit_element_creation(self) -> None:
        element = RevitElement(
            element_id="el-1",
            unique_id="uid-1",
            category_id="cat-1",
            category_name="Walls",
            class_name="Wall",
            family_name="Basic Wall",
            type_name="Generic - 8\"",
        )
        assert element.element_id == "el-1"
        assert element.category_name == "Walls"
        assert element.selected is False

    def test_revit_parameter_creation(self) -> None:
        param = RevitParameter(
            parameter_id="p1",
            name="Height",
            display_name="Height",
            storage_type=RevitParameterStorageType.DOUBLE,
            parameter_type=RevitParameterType.INSTANCE_PARAMETER,
            value=3.5,
            unit="meters",
        )
        assert param.value == 3.5
        assert param.unit == "meters"

    def test_revit_view_types(self) -> None:
        view = RevitView(view_id="v1", name="Level 1", view_type=RevitViewType.FLOOR_PLAN)
        assert view.view_type == RevitViewType.FLOOR_PLAN

    def test_revit_category_groups(self) -> None:
        cat = RevitCategory(category_id="cat-1", name="Walls", group=RevitCategoryGroup.ARCHITECTURAL)
        assert cat.group == RevitCategoryGroup.ARCHITECTURAL


class TestRevitRegistry:
    def test_register_capability(self) -> None:
        registry = RevitCapabilityRegistry()
        capability = RevitCapability(capability_id="cap-1", name="Read Elements", group="element", available=True)
        registry.register_capability(capability)
        assert registry.get_capability("cap-1") is not None

    def test_list_capabilities(self) -> None:
        registry = RevitCapabilityRegistry()
        registry.register_capability(RevitCapability(capability_id="cap-1", name="Read Elements", group="element", available=True))
        registry.register_capability(RevitCapability(capability_id="cap-2", name="Write Elements", group="element", available=False))
        assert len(registry.list_capabilities()) == 2

    def test_is_available(self) -> None:
        registry = RevitCapabilityRegistry()
        registry.register_capability(RevitCapability(capability_id="cap-1", name="Read Elements", group="element", available=True))
        registry.register_capability(RevitCapability(capability_id="cap-2", name="Write Elements", group="element", available=False))
        assert registry.is_available("cap-1") is True
        assert registry.is_available("cap-2") is False


class TestRevitDiscovery:
    def test_discover_returns_model_info(self) -> None:
        discovery = RevitDiscovery()
        info = discovery.discover()
        assert isinstance(info, RevitModelInfo)
        assert info.connection_state == "not_running"

    def test_discover_categories_returns_empty(self) -> None:
        discovery = RevitDiscovery()
        assert discovery.discover_categories() == []

    def test_discover_elements_returns_empty(self) -> None:
        discovery = RevitDiscovery()
        assert discovery.discover_elements() == []

    def test_discover_families_returns_empty(self) -> None:
        discovery = RevitDiscovery()
        assert discovery.discover_families() == []
