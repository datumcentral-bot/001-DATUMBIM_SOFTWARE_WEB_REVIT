from datetime import UTC, datetime

from desktop_agent.models import AgentCapabilities, AgentHealth


class HealthManager:
    def __init__(self, agent_id: str) -> None:
        self.agent_id = agent_id
        self._last_heartbeat: datetime | None = None
        self._uptime_seconds: int = 0
        self._error: str | None = None
        self._capabilities = AgentCapabilities()

    def record_heartbeat(self) -> None:
        self._last_heartbeat = datetime.now(tz=UTC)
        self._error = None

    def record_error(self, error: str) -> None:
        self._error = error

    def get_health(self) -> AgentHealth:
        return AgentHealth(
            agent_id=self.agent_id,
            status="online" if self._error is None else "error",
            last_heartbeat=self._last_heartbeat,
            uptime_seconds=self._uptime_seconds,
            error=self._error,
            capabilities=self._capabilities,
        )

    def set_capability(self, name: str, value: bool) -> None:
        setattr(self._capabilities, name, value)
