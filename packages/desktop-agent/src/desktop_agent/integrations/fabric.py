from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from desktop_agent.integrations.events import EventBus
from desktop_agent.integrations.models import (
    Integration,
    IntegrationEvent,
    IntegrationHealth,
    IntegrationRequest,
    IntegrationResult,
    IntegrationStatus,
    IntegrationType,
)
from desktop_agent.integrations.n8n import N8NConnector
from desktop_agent.integrations.registry import IntegrationRegistry
from desktop_agent.integrations.tools import ToolExecutionPipeline, ToolRegistry


class UniversalIntegrationFabric:
    def __init__(self) -> None:
        self.registry = IntegrationRegistry()
        self.tool_registry = ToolRegistry()
        self.tool_pipeline = ToolExecutionPipeline(self.tool_registry)
        self.event_bus = EventBus()
        self._n8n = N8NConnector()
        self._initialize_defaults()

    def _initialize_defaults(self) -> None:
        n8n_integration = self._n8n.to_integration()
        self.registry.register(n8n_integration)
        self.event_bus.subscribe(self._on_event, event_types=["integration.*", "tool.*"])

    def _on_event(self, event: IntegrationEvent) -> None:
        self.event_bus.publish("integration.event.received", source="integration_fabric", payload={"event_id": event.event_id, "event_type": event.event_type})

    def register_integration(self, integration: Integration) -> None:
        self.registry.register(integration)
        self.event_bus.publish("integration.registered", source="integration_fabric", payload={"integration_id": integration.integration_id, "type": integration.integration_type.value})

    def get_integration(self, integration_id: str) -> Integration | None:
        return self.registry.get(integration_id)

    def list_integrations(self, integration_type: IntegrationType | None = None, status: IntegrationStatus | None = None) -> list[Integration]:
        return self.registry.list(integration_type=integration_type, status=status)

    def connect(self, integration_id: str) -> IntegrationResult:
        integration = self.registry.get(integration_id)
        if not integration:
            return IntegrationResult(request_id="", status="failed", error="Integration not found", timestamp=datetime.now(tz=UTC))
        if integration_id == "n8n":
            result = self._n8n.connect()
            if result.status == "completed":
                self.registry.update_status(integration_id, IntegrationStatus.CONNECTED)
            return result
        self.registry.update_status(integration_id, IntegrationStatus.CONNECTED)
        return IntegrationResult(request_id="", status="completed", result={"message": "connected"}, timestamp=datetime.now(tz=UTC))

    def disconnect(self, integration_id: str) -> IntegrationResult:
        integration = self.registry.get(integration_id)
        if not integration:
            return IntegrationResult(request_id="", status="failed", error="Integration not found", timestamp=datetime.now(tz=UTC))
        if integration_id == "n8n":
            result = self._n8n.disconnect()
            self.registry.update_status(integration_id, IntegrationStatus.DISCONNECTED)
            return result
        self.registry.update_status(integration_id, IntegrationStatus.DISCONNECTED)
        return IntegrationResult(request_id="", status="completed", result={"message": "disconnected"}, timestamp=datetime.now(tz=UTC))

    def execute(self, request: IntegrationRequest) -> IntegrationResult:
        integration = self.registry.get(request.integration_id)
        if not integration:
            return IntegrationResult(request_id=request.request_id, status="failed", error="Integration not found", timestamp=datetime.now(tz=UTC))
        if request.integration_id == "n8n":
            if request.capability_id == "n8n_execute_workflow":
                workflow_id = request.parameters.get("workflow_id", "")
                return self._n8n.execute_workflow(workflow_id, request.parameters)
            if request.capability_id == "n8n_trigger_webhook":
                webhook_id = request.parameters.get("webhook_id", "")
                return self._n8n.trigger_webhook(webhook_id, request.parameters)
            if request.capability_id == "n8n_list_workflows":
                workflows = self._n8n.list_workflows()
                return IntegrationResult(request_id=request.request_id, status="completed", result={"workflows": workflows}, timestamp=datetime.now(tz=UTC))
        return self.tool_pipeline.execute(request)

    def health(self, integration_id: str) -> IntegrationHealth:
        integration = self.registry.get(integration_id)
        if not integration:
            return IntegrationHealth(integration_id=integration_id, status=IntegrationStatus.UNAVAILABLE, error="Integration not found", last_check=datetime.now(tz=UTC))
        if integration_id == "n8n":
            return self._n8n.health()
        return integration.health or IntegrationHealth(integration_id=integration_id, status=integration.status, last_check=datetime.now(tz=UTC))

    def register_tool(self, tool: dict[str, Any]) -> None:
        self.tool_registry.register_tool(tool)
        self.event_bus.publish("tool.registered", source="integration_fabric", payload={"tool_id": tool.get("tool_id"), "provider": tool.get("provider")})

    def list_tools(self, capability: str | None = None, provider: str | None = None) -> list[dict[str, Any]]:
        return self.tool_registry.list_tools(capability=capability, provider=provider)

    def get_events(self, event_type: str | None = None, source: str | None = None, limit: int = 100) -> list[IntegrationEvent]:
        return self.event_bus.get_events(event_type=event_type, source=source, limit=limit)

    def add_workflow(self, integration_id: str, workflow: Any) -> None:
        self.registry.add_workflow(integration_id, workflow)
        self.event_bus.publish("integration.workflow.added", source="integration_fabric", payload={"integration_id": integration_id, "workflow_id": workflow.workflow_id})

    def add_webhook(self, integration_id: str, webhook: Any) -> None:
        self.registry.add_webhook(integration_id, webhook)
        self.event_bus.publish("integration.webhook.added", source="integration_fabric", payload={"integration_id": integration_id, "webhook_id": webhook.webhook_id})
