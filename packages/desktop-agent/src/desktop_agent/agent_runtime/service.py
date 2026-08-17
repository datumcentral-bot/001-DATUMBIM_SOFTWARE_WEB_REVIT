from __future__ import annotations

from desktop_agent.agent_runtime.models import (
    AgentDefinition,
    AgentRun,
)
from desktop_agent.agent_runtime.orchestrator import AgentOrchestrator
from desktop_agent.execution.models import ToolDefinition
from desktop_agent.execution.service import ExecutionService


class AgentService:
    def __init__(self, execution_service: ExecutionService | None = None, orchestrator: AgentOrchestrator | None = None) -> None:
        self.execution_service = execution_service or ExecutionService()
        self.orchestrator = orchestrator or AgentOrchestrator(execution_service=self.execution_service)
        self._agents: dict[str, AgentDefinition] = {}

    def register_agent(self, agent: AgentDefinition) -> None:
        self._agents[agent.agent_id] = agent

    def get_agent(self, agent_id: str) -> AgentDefinition | None:
        return self._agents.get(agent_id)

    def list_agents(self, enabled_only: bool = False) -> list[AgentDefinition]:
        agents = list(self._agents.values())
        if enabled_only:
            agents = [a for a in agents if a.enabled]
        return agents

    def create_run(self, agent_id: str, goal: str, session_id: str | None = None, application_id: str | None = None, dry_run: bool = False) -> AgentRun | None:
        agent = self._agents.get(agent_id)
        if not agent or not agent.enabled:
            return None
        run = self.orchestrator.create_run(agent=agent, goal=goal, session_id=session_id, application_id=application_id, dry_run=dry_run)
        return run

    def start_run(self, run_id: str) -> AgentRun | None:
        for agent in self._agents.values():
            run = self.orchestrator.get_run(run_id)
            if run and run.agent_id == agent.agent_id:
                return self.orchestrator.start_run(agent, run)
        return None

    def get_run(self, run_id: str) -> AgentRun | None:
        return self.orchestrator.get_run(run_id)

    def cancel_run(self, run_id: str) -> AgentRun | None:
        return self.orchestrator.cancel_run(run_id)

    def approve_step(self, run_id: str, step_id: str, approved: bool = True) -> AgentRun | None:
        return self.orchestrator.approve_step(run_id, step_id, approved=approved)

    def register_tool(self, tool: ToolDefinition) -> None:
        self.execution_service.register_tool(tool)
