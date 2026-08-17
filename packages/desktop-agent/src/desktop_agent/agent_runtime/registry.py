from __future__ import annotations

from desktop_agent.agent_runtime.models import AgentDefinition


class AgentRegistry:
    def __init__(self) -> None:
        self._agents: dict[str, AgentDefinition] = {}

    def register(self, agent: AgentDefinition) -> None:
        self._agents[agent.agent_id] = agent

    def unregister(self, agent_id: str) -> bool:
        if agent_id in self._agents:
            del self._agents[agent_id]
            return True
        return False

    def get(self, agent_id: str) -> AgentDefinition | None:
        return self._agents.get(agent_id)

    def list(self, enabled_only: bool = False) -> list[AgentDefinition]:
        agents = list(self._agents.values())
        if enabled_only:
            agents = [a for a in agents if a.enabled]
        return agents

    def enable(self, agent_id: str) -> bool:
        agent = self._agents.get(agent_id)
        if not agent:
            return False
        self._agents[agent_id] = agent.model_copy(update={"enabled": True})
        return True

    def disable(self, agent_id: str) -> bool:
        agent = self._agents.get(agent_id)
        if not agent:
            return False
        self._agents[agent_id] = agent.model_copy(update={"enabled": False})
        return True

    def resolve(self, agent_id: str) -> AgentDefinition | None:
        agent = self._agents.get(agent_id)
        if not agent or not agent.enabled:
            return None
        return agent

    def get_tools(self, agent_id: str) -> list[str]:
        agent = self._agents.get(agent_id)
        if not agent:
            return []
        return list(agent.tools)

    def get_integrations(self, agent_id: str) -> list[str]:
        agent = self._agents.get(agent_id)
        if not agent:
            return []
        return list(agent.allowed_integrations)

    def get_applications(self, agent_id: str) -> list[str]:
        agent = self._agents.get(agent_id)
        if not agent:
            return []
        return list(agent.allowed_applications)

    def get_permissions(self, agent_id: str) -> list[str]:
        agent = self._agents.get(agent_id)
        if not agent:
            return []
        return list(agent.permissions)
