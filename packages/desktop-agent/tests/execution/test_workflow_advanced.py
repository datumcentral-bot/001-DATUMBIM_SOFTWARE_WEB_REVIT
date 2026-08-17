from __future__ import annotations

import pytest

from desktop_agent.execution.workflow import WorkflowEngine
from desktop_agent.execution.models import ExecutionMode, ExecutionRequest, ExecutionResult, ExecutionStatus, ToolDefinition, WorkflowDefinition


def test_workflow_conditional_step_not_implemented():
    engine = WorkflowEngine()
    wf = WorkflowDefinition(workflow_id="wf-cond", name="Conditional", description="Test", steps=[{"tool_id": "noop", "integration_id": "test", "condition": "true"}])
    engine.register_workflow(wf)
    engine.execution_runtime.register_tool(ToolDefinition(tool_id="noop", name="Noop", description="Test", category="test", provider="test", integration_id="test", execution_mode=ExecutionMode.LOCAL))
    execution = engine.execute("wf-cond", dry_run=True)
    assert execution.status == ExecutionStatus.SUCCEEDED


def test_workflow_failure_stops_execution():
    engine = WorkflowEngine()
    engine.execution_runtime.register_tool(ToolDefinition(tool_id="fail", name="Fail", description="Test", category="test", provider="test", integration_id="test", execution_mode=ExecutionMode.LOCAL))
    wf = WorkflowDefinition(workflow_id="wf-fail", name="Fail", description="Test", steps=[{"tool_id": "fail", "integration_id": "test"}, {"tool_id": "missing", "integration_id": "test"}])
    engine.register_workflow(wf)
    execution = engine.execute("wf-fail", dry_run=True)
    assert execution.status == ExecutionStatus.FAILED
    assert len(execution.steps) == 2
    assert execution.steps[-1]["status"] == "failed"


def test_workflow_approval_gate():
    engine = WorkflowEngine()
    engine.execution_runtime.register_tool(ToolDefinition(tool_id="approve", name="Approve", description="Test", category="test", provider="test", integration_id="test", requires_approval=True, execution_mode=ExecutionMode.LOCAL))
    wf = WorkflowDefinition(workflow_id="wf-approve", name="Approve", description="Test", steps=[{"tool_id": "approve", "integration_id": "test", "approval_required": True}])
    engine.register_workflow(wf)
    execution = engine.execute("wf-approve", dry_run=True)
    assert execution.status == ExecutionStatus.SUCCEEDED


def test_workflow_verification_failure_propagates():
    engine = WorkflowEngine()
    engine.execution_runtime.register_tool(ToolDefinition(tool_id="verify-fail", name="Verify Fail", description="Test", category="test", provider="test", integration_id="test", requires_verification=True, execution_mode=ExecutionMode.LOCAL))
    wf = WorkflowDefinition(workflow_id="wf-verify", name="Verify", description="Test", steps=[{"tool_id": "verify-fail", "integration_id": "test"}])
    engine.register_workflow(wf)
    execution = engine.execute("wf-verify", dry_run=True)
    assert execution.status == ExecutionStatus.SUCCEEDED


def test_workflow_sequential_steps_order():
    engine = WorkflowEngine()
    engine.execution_runtime.register_tool(ToolDefinition(tool_id="s1", name="S1", description="Test", category="test", provider="test", integration_id="test", execution_mode=ExecutionMode.LOCAL))
    engine.execution_runtime.register_tool(ToolDefinition(tool_id="s2", name="S2", description="Test", category="test", provider="test", integration_id="test", execution_mode=ExecutionMode.LOCAL))
    wf = WorkflowDefinition(workflow_id="wf-seq", name="Seq", description="Test", steps=[{"tool_id": "s1", "integration_id": "test"}, {"tool_id": "s2", "integration_id": "test"}])
    engine.register_workflow(wf)
    execution = engine.execute("wf-seq", dry_run=True)
    assert execution.status == ExecutionStatus.SUCCEEDED
    assert len(execution.steps) == 2
    assert execution.steps[0]["tool_id"] == "s1"
    assert execution.steps[1]["tool_id"] == "s2"
