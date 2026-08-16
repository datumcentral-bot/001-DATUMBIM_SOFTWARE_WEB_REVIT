from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from desktop_agent.integrations.models import (
    Integration,
    IntegrationCapability,
    IntegrationEvent,
    IntegrationHealth,
    IntegrationRequest,
    IntegrationResult,
    IntegrationStatus,
)


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, dict[str, Any]] = {}
        self._events: list[IntegrationEvent] = []

    def register_tool(self, tool: dict[str, Any]) -> None:
        tool_id = tool.get("tool_id")
        if not tool_id:
            return
        self._tools[tool_id] = tool
        self._emit("tool.registered", tool=tool)

    def unregister_tool(self, tool_id: str) -> None:
        tool = self._tools.pop(tool_id, None)
        if tool:
            self._emit("tool.unregistered", tool=tool)

    def get_tool(self, tool_id: str) -> dict[str, Any] | None:
        return self._tools.get(tool_id)

    def list_tools(self, capability: str | None = None, provider: str | None = None) -> list[dict[str, Any]]:
        tools = list(self._tools.values())
        if capability:
            tools = [t for t in tools if capability in t.get("capabilities", [])]
        if provider:
            tools = [t for t in tools if t.get("provider") == provider]
        return tools

    def resolve(self, capability: str, context: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        return self.list_tools(capability=capability)

    def _emit(self, event_type: str, **payload: Any) -> None:
        event = IntegrationEvent(
            event_id=f"evt-{datetime.now(tz=UTC).strftime('%Y%m%d%H%M%S%f')}",
            event_type=event_type,
            timestamp=datetime.now(tz=UTC),
            source="tool_registry",
            payload=payload,
        )
        self._events.append(event)

    def get_events(self, limit: int = 100) -> list[IntegrationEvent]:
        return self._events[-limit:]


class ToolExecutionPipeline:
    def __init__(self, tool_registry: ToolRegistry | None = None) -> None:
        self.tool_registry = tool_registry or ToolRegistry()

    def execute(self, request: IntegrationRequest) -> IntegrationResult:
        tool = self.tool_registry.get_tool(request.capability_id)
        if not tool:
            return IntegrationResult(
                request_id=request.request_id,
                status="failed",
                error=f"Tool not found: {request.capability_id}",
                timestamp=datetime.now(tz=UTC),
            )
        started = datetime.now(tz=UTC)
        try:
            result = tool.get("handler", lambda req: IntegrationResult(request_id=req.request_id, status="not_implemented", timestamp=datetime.now(tz=UTC)))(request)
            duration = (datetime.now(tz=UTC) - started).total_seconds() * 1000
            result.duration_ms = duration
            result.timestamp = datetime.now(tz=UTC)
            return result
        except Exception as exc:
            return IntegrationResult(
                request_id=request.request_id,
                status="failed",
                error=str(exc),
                timestamp=datetime.now(tz=UTC),
            )
