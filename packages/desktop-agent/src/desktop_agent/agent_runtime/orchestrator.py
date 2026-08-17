from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import Any

from desktop_agent.agent_runtime.models import (
    AgentDefinition,
    AgentRun,
    AgentRunStatus,
    AgentStepStatus,
    AutonomyLevel,
)
from desktop_agent.audit import AuditLogger
from desktop_agent.execution.models import (
    ExecutionRequest,
    ExecutionStatus,
)
from desktop_agent.execution.service import ExecutionService
from desktop_agent.integrations.events import EventBus
from desktop_agent.integrations.fabric import UniversalIntegrationFabric
from desktop_agent.permissions import PermissionEngine


class AgentOrchestrator:
    def __init__(
        self,
        execution_service: ExecutionService | None = None,
        integration_fabric: UniversalIntegrationFabric | None = None,
        permission_engine: PermissionEngine | None = None,
        audit_logger: AuditLogger | None = None,
        event_bus: EventBus | None = None,
    ) -> None:
        self.execution_service = execution_service or ExecutionService()
        self.integration_fabric = integration_fabric or UniversalIntegrationFabric()
        self.permission_engine = permission_engine or PermissionEngine()
        self.audit_logger = audit_logger or AuditLogger()
        self.event_bus = event_bus or EventBus()
        self._runs: dict[str, AgentRun] = {}

    def create_run(self, agent: AgentDefinition, goal: str, session_id: str | None = None, application_id: str | None = None, dry_run: bool = False) -> AgentRun:
        run_id = f"run-{uuid.uuid4().hex[:12]}"
        run = AgentRun(
            run_id=run_id,
            agent_id=agent.agent_id,
            goal=goal,
            status=AgentRunStatus.QUEUED,
            session_id=session_id,
            application_id=application_id,
            max_steps=agent.max_steps,
            created_at=datetime.now(tz=UTC),
            metadata={"dry_run": dry_run, "failure_policy": agent.failure_policy.value, "autonomy_level": agent.autonomy_level.value},
        )
        self._runs[run_id] = run
        self.event_bus.publish("agent.created", source="agent_orchestrator", payload={"run_id": run_id, "agent_id": agent.agent_id, "goal": goal})
        return run

    def start_run(self, agent: AgentDefinition, run: AgentRun) -> AgentRun:
        run.status = AgentRunStatus.PLANNING
        run.started_at = datetime.now(tz=UTC)
        self.event_bus.publish("agent.started", source="agent_orchestrator", payload={"run_id": run.run_id, "agent_id": agent.agent_id})
        try:
            plan = self._build_initial_plan(agent, run)
            run.steps.append(plan)
            if plan.get("approval_required") and agent.autonomy_level not in (AutonomyLevel.LEVEL_3, AutonomyLevel.LEVEL_4):
                run.status = AgentRunStatus.WAITING_APPROVAL
                self.event_bus.publish("agent.approval_required", source="agent_orchestrator", payload={"run_id": run.run_id, "step": plan.get("step_id")})
                return run
            run.status = AgentRunStatus.RUNNING
            self._execute_plan(agent, run, [plan])
        except Exception as exc:
            run.status = AgentRunStatus.FAILED
            run.error = str(exc)
            self.event_bus.publish("agent.failed", source="agent_orchestrator", payload={"run_id": run.run_id, "error": str(exc)})
        finally:
            run.completed_at = datetime.now(tz=UTC)
        return run

    def approve_step(self, run_id: str, step_id: str, approved: bool = True) -> AgentRun | None:
        run = self._runs.get(run_id)
        if not run:
            return None
        for step in run.steps:
            if step.get("step_id") == step_id:
                step["approval_state"] = "approved" if approved else "rejected"
                if not approved:
                    run.status = AgentRunStatus.CANCELLED
                    run.error = "Step rejected by user"
                    run.completed_at = datetime.now(tz=UTC)
                    self.event_bus.publish("agent.cancelled", source="agent_orchestrator", payload={"run_id": run_id})
                    return run
                break
        if run.status == AgentRunStatus.WAITING_APPROVAL:
            run.status = AgentRunStatus.RUNNING
            agent = self._resolve_agent(run.agent_id)
            if agent:
                plan = self._build_initial_plan(agent, run)
                self._execute_plan(agent, run, [plan])
        return run

    def cancel_run(self, run_id: str) -> AgentRun | None:
        run = self._runs.get(run_id)
        if not run:
            return None
        run.status = AgentRunStatus.CANCELLED
        run.completed_at = datetime.now(tz=UTC)
        self.event_bus.publish("agent.cancelled", source="agent_orchestrator", payload={"run_id": run_id})
        return run

    def get_run(self, run_id: str) -> AgentRun | None:
        return self._runs.get(run_id)

    def _resolve_agent(self, agent_id: str) -> AgentDefinition | None:
        registry = getattr(self.integration_fabric, "registry", None)
        if registry and hasattr(registry, "get_agent"):
            return registry.get_agent(agent_id)
        return None

    def _build_initial_plan(self, agent: AgentDefinition, run: AgentRun) -> dict[str, Any]:
        step_id = f"{run.run_id}-step-0"
        tool_id = agent.tools[0] if agent.tools else None
        tool = self.execution_service.get_tool(tool_id) if tool_id else None
        approval_required = bool(tool and tool.requires_approval)
        return {
            "step_id": step_id,
            "tool_id": tool_id,
            "parameters": {},
            "risk_level": tool.risk_level if tool else "low",
            "approval_required": approval_required,
            "status": "ready",
        }

    def _execute_plan(self, agent: AgentDefinition, run: AgentRun, plan: list[dict[str, Any]]) -> None:
        for action in plan:
            if run.current_step >= run.max_steps:
                run.status = AgentRunStatus.MAX_STEPS_REACHED
                run.error = "Maximum steps reached"
                self.event_bus.publish("agent.timeout", source="agent_orchestrator", payload={"run_id": run.run_id, "reason": "max_steps_reached"})
                return
            tool_id = action.get("tool_id")
            if not tool_id:
                continue
            tool = self.execution_service.get_tool(tool_id)
            if not tool:
                run.status = AgentRunStatus.FAILED
                run.error = f"Tool not found: {tool_id}"
                self.event_bus.publish("agent.failed", source="agent_orchestrator", payload={"run_id": run.run_id, "error": run.error})
                return
            if tool.availability not in ("available", "connected"):
                run.status = AgentRunStatus.FAILED
                run.error = f"Tool unavailable: {tool.availability}"
                self.event_bus.publish("agent.failed", source="agent_orchestrator", payload={"run_id": run.run_id, "error": run.error})
                return
            step = {
                "step_id": f"{run.run_id}-step-{run.current_step}",
                "run_id": run.run_id,
                "sequence": run.current_step,
                "goal": run.goal,
                "thought_summary": f"Selected tool {tool_id} for step {run.current_step}",
                "tool_id": tool_id,
                "parameters": action.get("parameters", {}),
                "status": AgentStepStatus.QUEUED.value,
                "approval_state": "pending",
                "started_at": datetime.now(tz=UTC).isoformat(),
                "metadata": {},
            }
            run.steps.append(step)
            run.current_step += 1
            self.event_bus.publish("agent.step_started", source="agent_orchestrator", payload={"run_id": run.run_id, "step_id": step.get("step_id"), "tool_id": tool_id})
            if run.metadata.get("dry_run"):
                step["status"] = AgentStepStatus.SUCCEEDED.value
                step["result"] = {"dry_run": True}
                self.event_bus.publish("agent.step_completed", source="agent_orchestrator", payload={"run_id": run.run_id, "step_id": step.get("step_id"), "status": "succeeded"})
                continue
            req = ExecutionRequest(
                execution_id=f"{run.run_id}-{step.get('step_id')}",
                tool_id=tool_id,
                integration_id=tool.integration_id,
                application_id=tool.application_id,
                session_id=run.session_id,
                parameters=action.get("parameters", {}),
                risk_level=action.get("risk_level", tool.risk_level),
                approval_required=action.get("approval_required", tool.requires_approval),
                approval_state="approved" if agent.autonomy_level in (AutonomyLevel.LEVEL_3, AutonomyLevel.LEVEL_4) else "pending",
                dry_run=run.metadata.get("dry_run", False),
                created_at=datetime.now(tz=UTC),
            )
            result = self.execution_service.execute(req)
            step["execution_id"] = result.execution_id
            step["status"] = result.status.value
            step["result"] = result.result
            step["error"] = result.error
            step["verification_state"] = result.verification_state
            if result.status == ExecutionStatus.SUCCEEDED:
                step["status"] = AgentStepStatus.SUCCEEDED.value
                self.event_bus.publish("agent.step_completed", source="agent_orchestrator", payload={"run_id": run.run_id, "step_id": step.get("step_id"), "status": "succeeded"})
            elif result.status == ExecutionStatus.WAITING_APPROVAL:
                step["status"] = AgentStepStatus.WAITING_APPROVAL.value
                run.status = AgentRunStatus.WAITING_APPROVAL
                self.event_bus.publish("agent.approval_required", source="agent_orchestrator", payload={"run_id": run.run_id, "step_id": step.get("step_id")})
                return
            else:
                step["status"] = AgentStepStatus.FAILED.value
                run.status = AgentRunStatus.FAILED
                run.error = result.error
                self.event_bus.publish("agent.failed", source="agent_orchestrator", payload={"run_id": run.run_id, "step_id": step.get("step_id"), "error": result.error})
                return
        run.status = AgentRunStatus.SUCCEEDED
        self.event_bus.publish("agent.completed", source="agent_orchestrator", payload={"run_id": run.run_id, "status": "succeeded"})
