from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from desktop_agent.execution.models import (
    ExecutionRequest,
    ExecutionStatus,
    WorkflowDefinition,
    WorkflowExecution,
)
from desktop_agent.execution.runtime import UniversalExecutionRuntime


class WorkflowEngine:
    def __init__(self, execution_runtime: UniversalExecutionRuntime | None = None) -> None:
        self.execution_runtime = execution_runtime or UniversalExecutionRuntime()
        self._workflows: dict[str, WorkflowDefinition] = {}
        self._executions: dict[str, WorkflowExecution] = {}

    def register_workflow(self, workflow: WorkflowDefinition) -> None:
        self._workflows[workflow.workflow_id] = workflow

    def get_workflow(self, workflow_id: str) -> WorkflowDefinition | None:
        return self._workflows.get(workflow_id)

    def list_workflows(self) -> list[WorkflowDefinition]:
        return list(self._workflows.values())

    def execute(self, workflow_id: str, inputs: dict[str, Any] | None = None, dry_run: bool = False) -> WorkflowExecution:
        workflow = self._workflows.get(workflow_id)
        if not workflow:
            raise ValueError(f"Workflow not found: {workflow_id}")
        execution_id = f"wf-{datetime.now(tz=UTC).strftime('%Y%m%d%H%M%S%f')}"
        execution = WorkflowExecution(execution_id=execution_id, workflow_id=workflow_id, status=ExecutionStatus.QUEUED, inputs=inputs or {}, steps=[], metadata={"workflow_steps": workflow.steps})
        self._executions[execution_id] = execution
        execution.status = ExecutionStatus.RUNNING
        execution.started_at = datetime.now(tz=UTC)
        try:
            for index, step in enumerate(workflow.steps):
                execution.current_step = index
                tool_id = step.get("tool_id")
                parameters = step.get("parameters", {})
                req = ExecutionRequest(execution_id=f"{execution_id}-step-{index}", tool_id=tool_id, integration_id=step.get("integration_id", ""), application_id=step.get("application_id"), session_id=step.get("session_id"), parameters=parameters, risk_level=step.get("risk_level", "low"), approval_required=step.get("approval_required", False), dry_run=dry_run, created_at=datetime.now(tz=UTC))
                result = self.execution_runtime.execute(req)
                execution.steps.append({"step": index, "tool_id": tool_id, "status": result.status.value, "result": result.result, "error": result.error})
                if result.status == ExecutionStatus.FAILED:
                    execution.status = ExecutionStatus.FAILED
                    execution.error = result.error
                    break
            else:
                execution.status = ExecutionStatus.SUCCEEDED
        except Exception as exc:
            execution.status = ExecutionStatus.FAILED
            execution.error = str(exc)
        finally:
            execution.completed_at = datetime.now(tz=UTC)
            if execution.started_at:
                execution.duration = (execution.completed_at - execution.started_at).total_seconds()
        return execution
