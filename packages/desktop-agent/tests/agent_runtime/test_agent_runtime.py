from __future__ import annotations

from desktop_agent.agent_runtime.models import (
    AgentDefinition,
    AgentRunStatus,
    AgentStepStatus,
    AutonomyLevel,
    FailurePolicy,
)
from desktop_agent.agent_runtime.orchestrator import AgentOrchestrator
from desktop_agent.agent_runtime.registry import AgentRegistry
from desktop_agent.agent_runtime.service import AgentService
from desktop_agent.execution.models import ExecutionMode, ToolDefinition
from desktop_agent.execution.service import ExecutionService


def test_agent_registry_register_and_resolve():
    registry = AgentRegistry()
    agent = AgentDefinition(agent_id="a1", name="Test Agent", description="Test", tools=["tool-1"], autonomy_level=AutonomyLevel.LEVEL_2)
    registry.register(agent)
    assert registry.get("a1") is not None
    assert registry.resolve("a1") is not None
    assert registry.resolve("missing") is None


def test_agent_registry_disable_hides_from_resolve():
    registry = AgentRegistry()
    agent = AgentDefinition(agent_id="a2", name="Disabled", description="Test", enabled=False, autonomy_level=AutonomyLevel.LEVEL_2)
    registry.register(agent)
    assert registry.resolve("a2") is None
    assert registry.enable("a2") is True
    assert registry.resolve("a2") is not None


def test_agent_registry_list_filters_enabled():
    registry = AgentRegistry()
    registry.register(AgentDefinition(agent_id="a3", name="Enabled", description="Test", enabled=True, autonomy_level=AutonomyLevel.LEVEL_2))
    registry.register(AgentDefinition(agent_id="a4", name="Disabled", description="Test", enabled=False, autonomy_level=AutonomyLevel.LEVEL_2))
    assert len(registry.list()) == 2
    assert len(registry.list(enabled_only=True)) == 1


def test_agent_registry_tool_and_integration_lists():
    registry = AgentRegistry()
    agent = AgentDefinition(agent_id="a5", name="Tools", description="Test", tools=["t1", "t2"], allowed_integrations=["n8n"], allowed_applications=["revit"], autonomy_level=AutonomyLevel.LEVEL_2)
    registry.register(agent)
    assert registry.get_tools("a5") == ["t1", "t2"]
    assert registry.get_integrations("a5") == ["n8n"]
    assert registry.get_applications("a5") == ["revit"]


def test_agent_service_create_and_start_run():
    service = AgentService()
    agent = AgentDefinition(agent_id="a6", name="Runner", description="Test", tools=["noop"], autonomy_level=AutonomyLevel.LEVEL_2)
    service.register_agent(agent)
    run = service.create_run(agent_id="a6", goal="test", dry_run=True)
    assert run.status == AgentRunStatus.QUEUED
    started = service.start_run(run.run_id)
    assert started.status in (AgentRunStatus.SUCCEEDED, AgentRunStatus.WAITING_APPROVAL, AgentRunStatus.FAILED)


def test_agent_service_unknown_agent_returns_none():
    service = AgentService()
    assert service.get_agent("missing") is None
    assert service.create_run(agent_id="missing", goal="test") is None


def test_agent_orchestrator_unknown_tool_fails_run():
    orchestrator = AgentOrchestrator()
    agent = AgentDefinition(agent_id="a7", name="Fail", description="Test", tools=["missing-tool"], autonomy_level=AutonomyLevel.LEVEL_2)
    run = orchestrator.create_run(agent=agent, goal="test", dry_run=True)
    result = orchestrator.start_run(agent, run)
    assert result.status == AgentRunStatus.FAILED
    assert "Tool not found" in (result.error or "")


def test_agent_orchestrator_dry_run_succeeds():
    orchestrator = AgentOrchestrator()
    service = ExecutionService()
    service.register_tool(ToolDefinition(tool_id="dry-tool", name="Dry", description="Test", category="test", provider="test", integration_id="test", execution_mode=ExecutionMode.LOCAL))
    orchestrator.execution_service = service
    agent = AgentDefinition(agent_id="a8", name="Dry", description="Test", tools=["dry-tool"], autonomy_level=AutonomyLevel.LEVEL_2)
    run = orchestrator.create_run(agent=agent, goal="dry run", dry_run=True)
    result = orchestrator.start_run(agent, run)
    assert result.status == AgentRunStatus.SUCCEEDED


def test_agent_orchestrator_approval_gate():
    orchestrator = AgentOrchestrator()
    service = ExecutionService()
    service.register_tool(ToolDefinition(tool_id="tool-approve", name="Approve", description="Test", category="test", provider="test", integration_id="test", requires_approval=True, execution_mode=ExecutionMode.LOCAL))
    orchestrator.execution_service = service
    agent = AgentDefinition(agent_id="a9", name="Approve", description="Test", tools=["tool-approve"], autonomy_level=AutonomyLevel.LEVEL_2)
    run = orchestrator.create_run(agent=agent, goal="approval test", dry_run=True)
    result = orchestrator.start_run(agent, run)
    assert result.status == AgentRunStatus.WAITING_APPROVAL


def test_agent_orchestrator_max_steps_protection():
    orchestrator = AgentOrchestrator()
    agent = AgentDefinition(agent_id="a10", name="Steps", description="Test", tools=["tool-1"], max_steps=1, autonomy_level=AutonomyLevel.LEVEL_2)
    run = orchestrator.create_run(agent=agent, goal="max steps", dry_run=True)
    run.current_step = 1
    result = orchestrator.start_run(agent, run)
    assert result.status == AgentRunStatus.MAX_STEPS_REACHED


def test_agent_run_statuses_and_step_statuses():
    assert AgentRunStatus.QUEUED.value == "queued"
    assert AgentRunStatus.PLANNING.value == "planning"
    assert AgentRunStatus.WAITING_APPROVAL.value == "waiting_approval"
    assert AgentRunStatus.RUNNING.value == "running"
    assert AgentRunStatus.SUCCEEDED.value == "succeeded"
    assert AgentRunStatus.FAILED.value == "failed"
    assert AgentRunStatus.CANCELLED.value == "cancelled"
    assert AgentRunStatus.TIMEOUT.value == "timeout"
    assert AgentRunStatus.MAX_STEPS_REACHED.value == "max_steps_reached"
    assert AgentStepStatus.QUEUED.value == "queued"
    assert AgentStepStatus.RUNNING.value == "running"
    assert AgentStepStatus.SUCCEEDED.value == "succeeded"
    assert AgentStepStatus.FAILED.value == "failed"


def test_agent_failure_policy_values():
    assert FailurePolicy.FAIL_FAST.value == "fail_fast"
    assert FailurePolicy.RETRY.value == "retry"
    assert FailurePolicy.REPLAN.value == "replan"
    assert FailurePolicy.FALLBACK_TOOL.value == "fallback_tool"
    assert FailurePolicy.ASK_USER.value == "ask_user"


def test_agent_autonomy_level_values():
    assert AutonomyLevel.LEVEL_0.value == "level_0"
    assert AutonomyLevel.LEVEL_4.value == "level_4"
