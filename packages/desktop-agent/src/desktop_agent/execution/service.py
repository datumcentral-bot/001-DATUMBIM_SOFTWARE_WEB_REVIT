from __future__ import annotations

from typing import Any

from desktop_agent.execution.models import (
    ExecutionRequest,
    ExecutionResult,
    ToolDefinition,
    WorkflowDefinition,
    WorkflowExecution,
)
from desktop_agent.execution.runtime import UniversalExecutionRuntime
from desktop_agent.execution.workflow import WorkflowEngine


class ExecutionService:
    def __init__(self, runtime: UniversalExecutionRuntime | None = None, workflow_engine: WorkflowEngine | None = None) -> None:
        self.runtime = runtime or UniversalExecutionRuntime()
        self.workflow_engine = workflow_engine or WorkflowEngine(self.runtime)
        self._executions: dict[str, ExecutionResult] = {}

    def register_tool(self, tool: ToolDefinition) -> None:
        self.runtime.register_tool(tool)

    def list_tools(self, capability: str | None = None, provider: str | None = None, integration_id: str | None = None, available_only: bool = False) -> list[ToolDefinition]:
        return self.runtime.list_tools(capability=capability, provider=provider, integration_id=integration_id, available_only=available_only)

    def get_tool(self, tool_id: str) -> ToolDefinition | None:
        return self.runtime.get_tool(tool_id)

    def execute(self, request: ExecutionRequest) -> ExecutionResult:
        result = self.runtime.execute(request)
        self._executions[request.execution_id] = result
        return result

    def get_execution(self, execution_id: str) -> ExecutionResult | None:
        return self._executions.get(execution_id)

    def register_workflow(self, workflow: WorkflowDefinition) -> None:
        self.workflow_engine.register_workflow(workflow)

    def list_workflows(self) -> list[WorkflowDefinition]:
        return self.workflow_engine.list_workflows()

    def get_workflow(self, workflow_id: str) -> WorkflowDefinition | None:
        return self.workflow_engine.get_workflow(workflow_id)

    def run_workflow(self, workflow_id: str, inputs: dict[str, Any] | None = None, dry_run: bool = False) -> WorkflowExecution:
        return self.workflow_engine.execute(workflow_id, inputs=inputs, dry_run=dry_run)
