import pytest

from desktop_agent.execution.models import (
    ExecutionMode,
    ExecutionStatus,
    ToolDefinition,
    WorkflowDefinition,
)
from desktop_agent.execution.workflow import WorkflowEngine


def test_workflow_register_and_list():
    engine = WorkflowEngine()
    wf = WorkflowDefinition(workflow_id="wf-1", name="Test Workflow", description="Test", steps=[])
    engine.register_workflow(wf)
    assert engine.get_workflow("wf-1") is not None
    assert len(engine.list_workflows()) == 1


def test_workflow_execute_success():
    engine = WorkflowEngine()
    engine.execution_runtime.register_tool(ToolDefinition(tool_id="noop", name="Noop", description="Test", category="test", provider="test", integration_id="test", execution_mode=ExecutionMode.LOCAL))
    wf = WorkflowDefinition(workflow_id="wf-success", name="Success", description="Test", steps=[{"tool_id": "noop", "integration_id": "test"}])
    engine.register_workflow(wf)
    execution = engine.execute("wf-success", dry_run=True)
    assert execution.status == ExecutionStatus.SUCCEEDED
    assert execution.workflow_id == "wf-success"
    assert len(execution.steps) == 1


def test_workflow_execute_missing_workflow():
    engine = WorkflowEngine()
    with pytest.raises(ValueError):
        engine.execute("missing")
