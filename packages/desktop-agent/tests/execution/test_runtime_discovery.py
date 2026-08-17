from __future__ import annotations

import pytest

from desktop_agent.execution.runtime import UniversalExecutionRuntime
from desktop_agent.execution.models import ExecutionMode, ExecutionRequest, ExecutionResult, ExecutionStatus, ToolDefinition


def test_runtime_discovery_by_capability():
    runtime = UniversalExecutionRuntime()
    runtime.register_tool(ToolDefinition(tool_id="t1", name="T1", description="Test", category="test", provider="test", integration_id="test", capabilities=["read"], execution_mode=ExecutionMode.LOCAL))
    runtime.register_tool(ToolDefinition(tool_id="t2", name="T2", description="Test", category="test", provider="test", integration_id="test", capabilities=["write"], execution_mode=ExecutionMode.LOCAL))
    tools = runtime.list_tools(capability="read")
    assert len(tools) == 1
    assert tools[0].tool_id == "t1"


def test_runtime_discovery_by_provider():
    runtime = UniversalExecutionRuntime()
    runtime.register_tool(ToolDefinition(tool_id="t1", name="T1", description="Test", category="test", provider="alpha", integration_id="test", execution_mode=ExecutionMode.LOCAL))
    runtime.register_tool(ToolDefinition(tool_id="t2", name="T2", description="Test", category="test", provider="beta", integration_id="test", execution_mode=ExecutionMode.LOCAL))
    tools = runtime.list_tools(provider="alpha")
    assert len(tools) == 1
    assert tools[0].provider == "alpha"


def test_runtime_available_only_filter():
    runtime = UniversalExecutionRuntime()
    runtime.register_tool(ToolDefinition(tool_id="t1", name="T1", description="Test", category="test", provider="test", integration_id="test", enabled=True, availability="available", execution_mode=ExecutionMode.LOCAL))
    runtime.register_tool(ToolDefinition(tool_id="t2", name="T2", description="Test", category="test", provider="test", integration_id="test", enabled=False, availability="unavailable", execution_mode=ExecutionMode.LOCAL))
    tools = runtime.list_tools(available_only=True)
    assert len(tools) == 1
    assert tools[0].tool_id == "t1"


def test_runtime_duplicate_registration_overwrites():
    runtime = UniversalExecutionRuntime()
    tool1 = ToolDefinition(tool_id="dup", name="Old", description="Test", category="test", provider="test", integration_id="test", execution_mode=ExecutionMode.LOCAL)
    tool2 = ToolDefinition(tool_id="dup", name="New", description="Test", category="test", provider="test", integration_id="test", execution_mode=ExecutionMode.LOCAL)
    runtime.register_tool(tool1)
    runtime.register_tool(tool2)
    assert runtime.get_tool("dup").name == "New"


def test_runtime_invalid_tool_id_returns_failed():
    runtime = UniversalExecutionRuntime()
    req = ExecutionRequest(execution_id="e1", tool_id="", integration_id="test", created_at=__import__("datetime").datetime.now(__import__("datetime").timezone.utc))
    result = runtime.execute(req)
    assert result.status == ExecutionStatus.FAILED


def test_runtime_execute_returns_audit_trail():
    runtime = UniversalExecutionRuntime()
    tool = ToolDefinition(tool_id="audit-tool", name="Audit Tool", description="Test", category="test", provider="test", integration_id="test", execution_mode=ExecutionMode.LOCAL)
    runtime.register_tool(tool)
    req = ExecutionRequest(execution_id="e-audit", tool_id="audit-tool", integration_id="test", dry_run=True, created_at=__import__("datetime").datetime.now(__import__("datetime").timezone.utc))
    result = runtime.execute(req)
    assert result.status == ExecutionStatus.SUCCEEDED
    entries = runtime.audit_logger.get_entries()
    assert len(entries) == 1
    assert entries[0].id == "e-audit"
