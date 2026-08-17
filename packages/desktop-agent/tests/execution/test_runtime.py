
from desktop_agent.execution.models import (
    ExecutionMode,
    ExecutionRequest,
    ExecutionStatus,
    ToolDefinition,
)
from desktop_agent.execution.runtime import UniversalExecutionRuntime


def test_runtime_registers_and_resolves_tool():
    runtime = UniversalExecutionRuntime()
    tool = ToolDefinition(tool_id="test-tool", name="Test Tool", description="Test", category="test", provider="test", integration_id="test", execution_mode=ExecutionMode.LOCAL)
    runtime.register_tool(tool)
    assert runtime.get_tool("test-tool") is not None
    assert len(runtime.list_tools()) == 1


def test_execute_unknown_tool_returns_failed():
    runtime = UniversalExecutionRuntime()
    req = ExecutionRequest(execution_id="1", tool_id="missing", integration_id="test", created_at=__import__("datetime").datetime.now(__import__("datetime").timezone.utc))
    result = runtime.execute(req)
    assert result.status == ExecutionStatus.FAILED
    assert "Tool not found" in (result.error or "")


def test_execute_disabled_tool_returns_unavailable():
    runtime = UniversalExecutionRuntime()
    tool = ToolDefinition(tool_id="disabled-tool", name="Disabled", description="Test", category="test", provider="test", integration_id="test", enabled=False, execution_mode=ExecutionMode.LOCAL)
    runtime.register_tool(tool)
    req = ExecutionRequest(execution_id="2", tool_id="disabled-tool", integration_id="test", created_at=__import__("datetime").datetime.now(__import__("datetime").timezone.utc))
    result = runtime.execute(req)
    assert result.status == ExecutionStatus.UNAVAILABLE


def test_execute_dry_run_succeeds():
    runtime = UniversalExecutionRuntime()
    tool = ToolDefinition(tool_id="dry-tool", name="Dry Tool", description="Test", category="test", provider="test", integration_id="test", execution_mode=ExecutionMode.LOCAL)
    runtime.register_tool(tool)
    req = ExecutionRequest(execution_id="3", tool_id="dry-tool", integration_id="test", dry_run=True, created_at=__import__("datetime").datetime.now(__import__("datetime").timezone.utc))
    result = runtime.execute(req)
    assert result.status == ExecutionStatus.SUCCEEDED
    assert result.result == {"dry_run": True, "tool_id": "dry-tool", "parameters": {}}


def test_execute_requires_approval_waiting():
    runtime = UniversalExecutionRuntime()
    tool = ToolDefinition(tool_id="approval-tool", name="Approval Tool", description="Test", category="test", provider="test", integration_id="test", requires_approval=True, execution_mode=ExecutionMode.LOCAL)
    runtime.register_tool(tool)
    req = ExecutionRequest(execution_id="4", tool_id="approval-tool", integration_id="test", approval_required=True, approval_state="pending", created_at=__import__("datetime").datetime.now(__import__("datetime").timezone.utc))
    result = runtime.execute(req)
    assert result.status == ExecutionStatus.WAITING_APPROVAL


def test_execute_unavailable_integration():
    runtime = UniversalExecutionRuntime()
    tool = ToolDefinition(tool_id="api-tool", name="API Tool", description="Test", category="api", provider="test", integration_id="missing", execution_mode=ExecutionMode.API)
    runtime.register_tool(tool)
    req = ExecutionRequest(execution_id="5", tool_id="api-tool", integration_id="missing", created_at=__import__("datetime").datetime.now(__import__("datetime").timezone.utc))
    result = runtime.execute(req)
    assert result.status == ExecutionStatus.UNAVAILABLE
