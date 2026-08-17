from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from desktop_agent.audit import AuditLogger
from desktop_agent.execution.models import (
    ExecutionMode,
    ExecutionRequest,
    ExecutionResult,
    ExecutionStatus,
    ToolDefinition,
)
from desktop_agent.integrations.fabric import UniversalIntegrationFabric
from desktop_agent.permissions import PermissionEngine


class UniversalExecutionRuntime:
    def __init__(
        self,
        integration_fabric: UniversalIntegrationFabric | None = None,
        permission_engine: PermissionEngine | None = None,
        audit_logger: AuditLogger | None = None,
    ) -> None:
        self.integration_fabric = integration_fabric or UniversalIntegrationFabric()
        self.permission_engine = permission_engine or PermissionEngine()
        self.audit_logger = audit_logger or AuditLogger()
        self._tools: dict[str, ToolDefinition] = {}

    def register_tool(self, tool: ToolDefinition) -> None:
        self._tools[tool.tool_id] = tool
        self.integration_fabric.register_tool(tool.model_dump())

    def get_tool(self, tool_id: str) -> ToolDefinition | None:
        return self._tools.get(tool_id)

    def list_tools(self, capability: str | None = None, provider: str | None = None, integration_id: str | None = None, available_only: bool = False) -> list[ToolDefinition]:
        tools = list(self._tools.values())
        if capability:
            tools = [t for t in tools if capability in t.capabilities]
        if provider:
            tools = [t for t in tools if t.provider == provider]
        if integration_id:
            tools = [t for t in tools if t.integration_id == integration_id]
        if available_only:
            tools = [t for t in tools if t.availability in ("available", "connected") and t.enabled]
        return tools

    def execute(self, request: ExecutionRequest) -> ExecutionResult:
        started_at = datetime.now(tz=UTC)
        tool = self._tools.get(request.tool_id)
        if not tool:
            self.audit_logger.log(self._build_audit(request, started_at, ExecutionStatus.FAILED, error=f"Tool not found: {request.tool_id}"))
            return ExecutionResult(execution_id=request.execution_id, status=ExecutionStatus.FAILED, error=f"Tool not found: {request.tool_id}", started_at=started_at, completed_at=datetime.now(tz=UTC))

        if not tool.enabled:
            self.audit_logger.log(self._build_audit(request, started_at, ExecutionStatus.UNAVAILABLE, error=f"Tool disabled: {request.tool_id}"))
            return ExecutionResult(execution_id=request.execution_id, status=ExecutionStatus.UNAVAILABLE, error=f"Tool disabled: {request.tool_id}", started_at=started_at, completed_at=datetime.now(tz=UTC))

        if tool.availability not in ("available", "connected"):
            self.audit_logger.log(self._build_audit(request, started_at, ExecutionStatus.UNAVAILABLE, error=f"Tool unavailable: {tool.availability}"))
            return ExecutionResult(execution_id=request.execution_id, status=ExecutionStatus.UNAVAILABLE, error=f"Tool unavailable: {tool.availability}", started_at=started_at, completed_at=datetime.now(tz=UTC))

        if request.approval_required and request.approval_state != "approved":
            self.audit_logger.log(self._build_audit(request, started_at, ExecutionStatus.WAITING_APPROVAL))
            return ExecutionResult(execution_id=request.execution_id, status=ExecutionStatus.WAITING_APPROVAL, started_at=started_at, completed_at=datetime.now(tz=UTC))

        if request.dry_run:
            self.audit_logger.log(self._build_audit(request, started_at, ExecutionStatus.SUCCEEDED, result={"dry_run": True, "tool_id": request.tool_id, "parameters": request.parameters}))
            return ExecutionResult(execution_id=request.execution_id, status=ExecutionStatus.SUCCEEDED, started_at=started_at, completed_at=datetime.now(tz=UTC), result={"dry_run": True, "tool_id": request.tool_id, "parameters": request.parameters})

        try:
            result = self._execute_tool(tool, request)
            result.started_at = started_at
            result.completed_at = datetime.now(tz=UTC)
            result.duration = (result.completed_at - started_at).total_seconds()
            self.audit_logger.log(self._build_audit(request, started_at, result.status, result=result.result, error=result.error, verification_state=result.verification_state))
            return result
        except Exception as exc:
            self.audit_logger.log(self._build_audit(request, started_at, ExecutionStatus.FAILED, error=str(exc)))
            return ExecutionResult(execution_id=request.execution_id, status=ExecutionStatus.FAILED, started_at=started_at, completed_at=datetime.now(tz=UTC), error=str(exc))

    def _execute_tool(self, tool: ToolDefinition, request: ExecutionRequest) -> ExecutionResult:
        if tool.execution_mode == ExecutionMode.API:
            return self._execute_api(tool, request)
        if tool.execution_mode == ExecutionMode.N8N:
            return self._execute_n8n(tool, request)
        if tool.execution_mode == ExecutionMode.DESKTOP:
            return self._execute_desktop(tool, request)
        if tool.execution_mode == ExecutionMode.APPLICATION:
            return self._execute_application(tool, request)
        if tool.execution_mode == ExecutionMode.AI:
            return self._execute_ai(tool, request)
        return ExecutionResult(execution_id=request.execution_id, status=ExecutionStatus.NOT_IMPLEMENTED, error=f"Execution mode not implemented: {tool.execution_mode}")

    def _execute_api(self, tool: ToolDefinition, request: ExecutionRequest) -> ExecutionResult:
        integration = self.integration_fabric.get_integration(request.integration_id)
        if not integration:
            return ExecutionResult(execution_id=request.execution_id, status=ExecutionStatus.UNAVAILABLE, error="Integration not found")
        return self.integration_fabric.execute(request)

    def _execute_n8n(self, tool: ToolDefinition, request: ExecutionRequest) -> ExecutionResult:
        integration = self.integration_fabric.get_integration("n8n")
        if not integration:
            return ExecutionResult(execution_id=request.execution_id, status=ExecutionStatus.UNAVAILABLE, error="n8n not configured")
        return self.integration_fabric.execute(request)

    def _execute_desktop(self, tool: ToolDefinition, request: ExecutionRequest) -> ExecutionResult:
        return ExecutionResult(execution_id=request.execution_id, status=ExecutionStatus.NOT_IMPLEMENTED, error="Desktop execution not yet implemented")

    def _execute_application(self, tool: ToolDefinition, request: ExecutionRequest) -> ExecutionResult:
        return ExecutionResult(execution_id=request.execution_id, status=ExecutionStatus.NOT_IMPLEMENTED, error="Application execution not yet implemented")

    def _execute_ai(self, tool: ToolDefinition, request: ExecutionRequest) -> ExecutionResult:
        return ExecutionResult(execution_id=request.execution_id, status=ExecutionStatus.NOT_IMPLEMENTED, error="AI execution not yet implemented")

    def _build_audit(self, request: ExecutionRequest, started_at: datetime, status: ExecutionStatus, result: Any = None, error: str | None = None, verification_state: str | None = None):
        from desktop_agent.models import AuditLogEntry
        duration_ms = None
        if request.created_at:
            duration_ms = int((datetime.now(tz=UTC) - request.created_at).total_seconds() * 1000)
        return AuditLogEntry(
            id=request.execution_id,
            agent_id=request.requested_by or "system",
            action=request.tool_id,
            target=request.integration_id,
            parameters={k: str(v) for k, v in request.parameters.items()},
            result=str(result)[:1000] if result is not None else "",
            timestamp=started_at,
            duration_ms=duration_ms,
            error=error or "",
            evidence=verification_state or "",
        )
