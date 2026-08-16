import pytest

from desktop_agent.integrations.fabric import UniversalIntegrationFabric
from desktop_agent.integrations.models import IntegrationStatus, IntegrationType
from desktop_agent.integrations.n8n import N8NConnector
from desktop_agent.integrations.registry import IntegrationRegistry
from desktop_agent.integrations.tools import ToolRegistry


def test_fabric_initializes_with_n8n():
    fabric = UniversalIntegrationFabric()
    integration = fabric.get_integration("n8n")
    assert integration is not None
    assert integration.integration_id == "n8n"
    assert integration.integration_type == IntegrationType.AUTOMATION


def test_fabric_register_integration():
    fabric = UniversalIntegrationFabric()
    integration = fabric.get_integration("n8n")
    assert integration is not None


def test_n8n_connector_defaults():
    connector = N8NConnector()
    assert connector.installed is False
    assert connector.status == IntegrationStatus.NOT_INSTALLED


def test_tool_register_and_list():
    registry = ToolRegistry()
    tool = {"tool_id": "test-tool", "name": "Test Tool", "provider": "test", "capabilities": ["test"]}
    registry.register_tool(tool)
    tools = registry.list_tools()
    assert len(tools) == 1
    assert tools[0]["tool_id"] == "test-tool"


def test_tool_resolve_by_capability():
    registry = ToolRegistry()
    tool = {"tool_id": "test-tool", "name": "Test Tool", "provider": "test", "capabilities": ["test"]}
    registry.register_tool(tool)
    resolved = registry.resolve("test")
    assert len(resolved) == 1
    assert resolved[0]["tool_id"] == "test-tool"


def test_integration_registry_session_lifecycle():
    registry = IntegrationRegistry()
    from desktop_agent.integrations.models import Integration
    integration = Integration(
        integration_id="test",
        name="Test",
        description="Test integration",
        integration_type=IntegrationType.API,
        status=IntegrationStatus.READY,
    )
    registry.register(integration)
    session = registry.start_session("test")
    assert session is not None
    assert session.status == IntegrationStatus.CONNECTED
    registry.end_session("test", session.session_id)
    assert session.status == IntegrationStatus.DISCONNECTED
